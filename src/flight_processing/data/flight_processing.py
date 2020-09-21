from ..process_flights import version, AirspaceHandler
from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between, lerp
from ..scalebar import scale_bar
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre, save_graph_to_file, process_dataframe
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
import holoviews as hv
import networkx as nx
import hvplot.networkx as hvnx
from traffic.core.flight import Flight
from traffic.core.traffic import Traffic

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

from traffic.data import opensky

class AirspaceGraph:
    def __init__(self, dataset, df=None, dataset_location=None, verbose=False):
        if isinstance(dataset, DataConfig):
            self.__data_config = dataset
            self.dataset = dataset.dataset
        elif isinstance(dataset, str):
            self.__data_config = DataConfig.known_dataset(dataset)
            self.dataset = dataset
        else:
            raise ValueError("Argument 'dataset' must be of type DataConfig or str.")

        print("Loading airspace dataset...")
        if df is not None:
            self.__gdf = process_dataframe(df)
        else:
            if dataset_location is None:
                dataset_location = self.__data_config.dataset_location

            self.__gdf = geopandas.read_file(dataset_location)

        print("Populating AirspaceHandler...")
        self.__airspaces = AirspaceHandler()
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)
        self.__gdf.set_index('ident', inplace=True)

        self.num_airspaces = self.__airspaces.size()

        print("Done!")

    def load_graphs(self, time_start, time_end):
        print("Loading graph of handovers...")
        self.__matrix = self.__load_npz_bulk(time_start, time_end)

        print("Building graph...")
        self.__graph = build_graph_from_sparse_matrix(self.__gdf, self.__matrix)

        print("Computing adjusted weights...")
        self.__graph_relative_weights()

        print("Done!")

    def load_graph_files(self, files):
        if isinstance(files, str):
            to_load = [files]
        elif isinstance(files, list) and all(isinstance(f, str) for f in files):
            to_load = files
        else:
            raise ValueError("Argument 'files' must be str or list of str.")

        print("Loading graph of handovers...")
        self.__matrix = self.__load_npz_files(to_load)

        print("Building graph...")
        self.__graph = build_graph_from_sparse_matrix(self.__gdf, self.__matrix)

        print("Computing adjusted weights...")
        self.__graph_relative_weights()

        print("Done!")

    def __load_npz_files(self, files):
        matrix = None

        for f in files:
            matrix_new = sparse.load_npz(f)
            if matrix is None:
                matrix = matrix_new
            else:
                matrix += matrix_new

        return matrix

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
        if isinstance(airspace, str):
            gdf_temp = self.__gdf[self.__gdf['name'] == airspace]
            if len(gdf_temp) == 0:
                return None
            return gdf_temp.iloc[0]
        elif isinstance(airspace, int):
            return self.__gdf.loc[airspace]
        else:
            try:
                a = int(airspace)
                return self.__gdf.loc[a]
            except:
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
        return hvnx.draw(self.__graph, mercator_positions(self.__gdf, self.__graph), edge_width=hv.dim('weight')*0.003, node_size=30, arrowhead_length=0.0001)

    def draw_graph_map(self, file_out=None, logscale=False):
        fig = plt.figure(dpi=300, figsize=(7,7))

        imagery = cimgt.Stamen(style="terrain-background")
        ax = plt.axes(projection=imagery.crs)

        ax.set_extent(self.__data_config.bounds_plt)

        ax.add_image(imagery, self.__data_config.detail)

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

    def average_edge_weight(self):
        weight_total = 0
        count = 0

        for source, dest, data in self.__graph.edges(data=True):
            if source != dest:
                weight_total += data.get('weight')
                count += 1

        return weight_total / count

    def __airspace_total_weight(self, name):
        total = 0
        for k, v in self.__graph[name].items():
            if k != name:
                total += v['weight']
        return total

    def __graph_relative_weights(self):
        self.__gdf['total_weight'] = self.__gdf['name'].apply(lambda x: self.__airspace_total_weight(x))

        for name in self.__graph.nodes:
            total_weight = self.__gdf[self.__gdf['name'] == name].iloc[0].total_weight
            for k, v in self.__graph[name].items():
                v['weight_adjusted'] = v['weight'] / total_weight if total_weight != 0 else 0

    def __confidence(self, edge, distance=None):
        if edge is not None:
            weight = edge.get('weight')
            weight_adjusted = edge.get('weight_adjusted')
        else:
            weight = 0
            weight_adjusted = 0

        # TODO put thresholds etc elsewhere
        threshold_distance_zero = 5000
        threshold_distance_one = 3000
        threshold_weight = 50
        threshold_weight_adjusted = 0.05

        if distance is not None:
            confidence_distance = lerp(distance, threshold_distance_one, threshold_distance_zero, 0.0, 1.0)
        else:
            confidence_distance = 0

        confidence_weight = weight >= threshold_weight
        confidence_weight_adjusted = weight_adjusted >= threshold_weight_adjusted

        confidence = confidence_distance + int(confidence_weight) + int(confidence_weight_adjusted)

        return dict(
            distance = distance,
            confidence = confidence,
            weight = weight,
            weight_adjusted = weight_adjusted,
            confidence_distance = confidence_distance,
            confidence_weight = confidence_weight,
            confidence_weight_adjusted = confidence_weight_adjusted
        )

    def process_single_flight(self, flight):
        xs = np.array([c[0] for c in list(flight.coords)])
        ys = np.array([c[1] for c in list(flight.coords)])
        hs = np.array([c[2] for c in list(flight.coords)])
        return self.__airspaces.process_single_flight(xs, ys, hs)

    def test_point(self, long, lat, height):
        ids_at_point = self.__airspaces.airspaces_at_point(long, lat, height)
        near_point = self.__airspaces.airspaces_near_point(long, lat, height)
        #ids_near_point = [ x[0] for x in near_point ]

        for id_at in ids_at_point:
            name_at = self.__gdf.loc[id_at]['name']
            print("At airspace {}. Potential handovers:".format(name_at))
            for (id_near, distance) in near_point:
                name_near = self.__gdf.loc[id_near]['name']
                edge = self.__graph[name_at].get(name_near)

                confidence = self.__confidence(edge, distance)

                print("- {}".format(name_near))
                print("  distance {:.0f} ft".format(distance))
                print("  edge weight {}".format(confidence['weight']))
                print("  confidence {}".format(confidence['confidence']))

    def test_handover(self, long, lat, height, airspace1, airspace2):
        a1 = self.get_airspace(airspace1)
        a2 = self.get_airspace(airspace2)
        if a1 is None or a2 is None:
            raise ValueError("Airspace not found!")

        edge = self.__graph[a1['name']].get(a2['name'])
        distance = self.__airspaces.distance_to_airspace(long, lat, height, int(a2.name))

        confidence = self.__confidence(edge, distance)

        return confidence

    def test_flight(self, flight):
        if not isinstance(flight, Flight):
            raise ValueError("Argument must be of type Flight!")

        handovers = self.process_single_flight(flight)

        out = []

        for airspace1, airspace2 in handovers:
            a1 = self.get_airspace(airspace1)
            a2 = self.get_airspace(airspace2)

            edge = self.__graph[a1['name']].get(a2['name'])

            confidence = self.__confidence(edge)

            confidence['airspace1'] = a1.name
            confidence['airspace2'] = a2.name
            confidence['name1'] = a1['name']
            confidence['name2'] = a2['name']

            out.append(confidence)

        return out


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