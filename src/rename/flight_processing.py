from ..process_flights import version, AirspaceHandler
from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_withend
from .. import config

from scipy import sparse
from dateutil import parser
import math
import pandas as pd
import numpy as np
import geopandas
from shapely.geometry import Point
import networkx as nx
import hvplot.networkx as hvnx

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

from traffic.data import opensky

class AirspaceGraph:
    def __init__(self, dataset, time_start, time_end):
        self.__data_config = DataConfig(dataset)

        self.__matrix = self.__load_npz_bulk(time_start, time_end)

        self.__gdf = geopandas.read_file(self.__data_config.dataset_location)

        self.__airspaces = AirspaceHandler()
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)
        self.__gdf.set_index('ident', inplace=True)

        self.num_airspaces = self.__airspaces.size()

        self.__graph = build_graph_from_matrix(self.__gdf, self.__matrix)



    @classmethod
    def fromconfig(cls, dataset, time_start, time_end):
        return cls(dataset, time_start, time_end)

    @classmethod
    def withbounds(cls, dataset, time_start, time_end):
        return cls(dataset, time_start, time_end)

    def __load_npz(self, time):
        #file_load = graph_location_npz.format(dataset=dataset, date=time.strftime(timestring_date), time=time.strftime(timestring_time))
        file_load = self.__data_config.data_graph_npz(time)
        return sparse.load_npz(file_load)

    def __load_npz_bulk(self, time_start, time_end):
        t_start = parser.parse(time_start)
        t_end = parser.parse(time_end)
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
        return self.__graph[name1][name2]['weight']

    def zone_centre(self, name):
        return get_zone_centre(self.__gdf, name)

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
        positions_transformed = mercator_positions(self.__gdf, self.__graph)
        cmap = plt.cm.Purples

        nodes = nx.draw_networkx_nodes(graph, positions_transformed, ax=ax, node_size=5, node_color="red")
        edges = nx.draw_networkx_edges(graph, positions_transformed, ax=ax, node_size=5, edge_color=weights, edge_cmap=cmap, arrowsize=5, arrowstyle="->", width=0.8)
        nodes.set_zorder(20)
        for edge in edges:
            edge.set_zorder(19)

        scale_bar(ax, (0.75, 0.05), 100)

        ax.set_aspect('auto')

        if file_out is not None:
            plt.savefig(file_out, bbox_inches='tight', transparent=True)

        plt.show()

    def test_point(self, long, lat, height):
        pass

    def test_handover(self, long, lat, height, id_1, id_2):
        pass


def graph_add_node(graph, name):
    if not graph.has_node(name):
        graph.add_node(name)

def graph_increment_edge(graph, u, v, amount=1):
        if graph.has_edge(u, v):
            graph[u][v]['weight'] += amount
        else:
            graph.add_edge(u, v, weight=amount)

def build_graph_from_matrix(gdf, matrix):
    n, m = matrix.shape
    assert(n == m)

    graph = nx.DiGraph()
    for i in range(n):
        name = gdf.loc[i]['name']
        graph.add_node(graph, name)

    I, J, V = sparse.find(matrix)
    N = I.size

    for k in range(N):
        i = I[k]
        j = J[k]
        v = V[k]
        name_i = gdf.loc[i]['name']
        name_j = gdf.loc[j]['name']
        increment_edge(graph, name_i, name_j, v)

    return graph

def get_zone_centre(gdf, name):
    gdf_temp = gdf[gdf['name'] == name]
    if len(gdf_temp) == 0:
        return None
    if gdf_temp.iloc[0].geometry is None:
        return Point(0.0, 0.0)
    return gdf_temp.iloc[0].geometry.centroid

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