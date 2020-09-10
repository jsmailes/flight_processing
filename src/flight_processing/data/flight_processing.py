from ..process_flights import version, AirspaceHandler
from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between
from ..scalebar import scale_bar
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre
from .. import config

from scipy import sparse
from datetime import timedelta
from dateutil import parser
import math
import pandas as pd
import numpy as np
import geopandas
import pyproj
from shapely.geometry import Point
from shapely.ops import transform
import networkx as nx
import hvplot.networkx as hvnx

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

from traffic.data import opensky

class AirspaceGraph:
    def __init__(self, dataset, time_start, time_end):
        self.__data_config = DataConfig(dataset)

        print("Loading graph of handovers...")
        self.__matrix = self.__load_npz_bulk(time_start, time_end)

        print("Loading airspace dataset...")
        self.__gdf = geopandas.read_file(self.__data_config.dataset_location)

        print("Populating AirspaceHandler...")
        self.__airspaces = AirspaceHandler()
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)
        self.__gdf.set_index('ident', inplace=True)

        self.num_airspaces = self.__airspaces.size()

        print("Building graph...")
        self.__graph = build_graph_from_sparse_matrix(self.__gdf, self.__matrix)

        print("Done!")

    @classmethod # TODO
    def fromconfig(cls, dataset, time_start, time_end):
        return cls(dataset, time_start, time_end)

    @classmethod # TODO
    def withbounds(cls, dataset, time_start, time_end):
        return cls(dataset, time_start, time_end)

    def __load_npz(self, time):
        file_load = self.__data_config.data_graph_npz(time)
        return sparse.load_npz(file_load)

    def __load_npz_bulk(self, time_start, time_end):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))
        t_delta = timedelta(hours=1)
        count = math.floor((t_end - t_start) / t_delta)

        matrix = None

        for i in range(count):
            t = t_start + (i * t_delta)
            matrix_new = self.__load_npz(t)
            if matrix is None:
                matrix = matrix_new
            else:
                matrix += matrix_new

        return matrix

    def __add_airspace(self, row):
        return self.__airspaces.add_airspace(row.wkt, row.lower_limit, row.upper_limit)

    def get_airspace(self, airspace):
        if isinstance(airspace, int):
            return self.__gdf.loc[airspace]
        elif isinstance(airspace, str):
            gdf_temp = self.__gdf[self.__gdf['name'] == airspace]
            if len(gdf_temp) == 0:
                return None
            return gdf_temp.iloc[0]
        else:
            return None

    def edge_weight(self, airspace1, airspace2):
        name1 = self.get_airspace(airspace1)['name']
        name2 = self.get_airspace(airspace2)['name']
        edge = self.__graph[name1].get(name2)
        if edge is not None:
            weight = edge.get('weight')
            return weight if weight is not None else 0
        else:
            return 0

    def zone_centre(self, name):
        return get_zone_centre(self.__gdf, self.get_airspace(name)['name'])

    def visualise_graph(self):
        hvnx.draw(self.__graph, mercator_positions(self.__gdf, self.__graph), edge_width=hv.dim('weight')*0.003, node_size=30, arrowhead_length=0.0001)

    def draw_graph_map(self, file_out=None, logscale=False):
        fig = plt.figure(dpi=300, figsize=(7,7))

        imagery = cimgt.Stamen(style="terrain-background")
        ax = plt.axes(projection=imagery.crs)

        ax.set_extent(self.__data_config.bounds_plt)

        ax.add_image(imagery, self.__data_config.detail, interpolation='spline36', cmap="gray")

        ax.add_geometries(self.__gdf.geometry, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black") #"#8fa8bf"

        _, weights_original = zip(*nx.get_edge_attributes(self.__graph, 'weight').items())
        if logscale:
            weights = tuple(map(lambda x: math.log(x), weights_original))
        else:
            weights = weights_original
        positions_transformed = mercator_positions(self.__gdf, self.__graph)
        cmap = plt.cm.Purples

        nodes = nx.draw_networkx_nodes(self.__graph, positions_transformed, ax=ax, node_size=5, node_color="red")
        edges = nx.draw_networkx_edges(self.__graph, positions_transformed, ax=ax, node_size=5, edge_color=weights, edge_cmap=cmap, arrowsize=5, arrowstyle="->", width=0.8)
        nodes.set_zorder(20)
        for edge in edges:
            edge.set_zorder(19)

        scale_bar(ax, (0.75, 0.05), 100)

        ax.set_aspect('auto')

        if file_out is not None:
            plt.savefig(file_out, bbox_inches='tight', transparent=True)

        plt.show()

    def test_point(self, long, lat, height): # TODO
        pass

    def test_handover(self, long, lat, height, id_1, id_2): # TODO
        pass


wgs84 = pyproj.CRS('EPSG:4326')
mercator = pyproj.CRS('EPSG:3857') # Note: if we change the map source this will need to change too!
wgs84_to_mercator = pyproj.Transformer.from_crs(wgs84, mercator, always_xy=True).transform

def point_to_mercator(point):
    return transform(wgs84_to_mercator, point)

def mercator_positions(gdf, graph):
    positions_transformed = dict()
    for name in list(nx.nodes(graph)):
        positions_transformed[name] = list(point_to_mercator(get_zone_centre(gdf, name)).coords)[0]
    return positions_transformed