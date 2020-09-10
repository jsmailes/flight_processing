from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between
from ..process_flights import version, AirspaceHandler
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre, save_graph_to_file

from datetime import datetime, timedelta
from dateutil import parser
from scipy import sparse
import geopandas
from shapely.geometry import Point

import networkx as nx

class GraphBuilder:
    def __add_airspace(self, row):
        return self.__airspaces.add_airspace(row.wkt, row.lower_limit, row.upper_limit)

    def __init__(self, dataset, verbose=False):
        self.dataset = dataset
        self.verbose = verbose

        self.__data_config = DataConfig(dataset=dataset)

        if self.verbose:
            print("Loading airspace data from {}.".format(self.__data_config.dataset_location))
        self.__gdf = geopandas.read_file(self.__data_config.dataset_location)

        self.__airspaces = AirspaceHandler()

        if self.verbose:
            print("Adding airspace data to C++.")
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)

    def process_flights(self, time, json=False, yaml=False, npz=True):
        t = parser.parse(str(time))

        if self.verbose:
            print("Processing data for {}.".format(t))

        data_flights = self.__data_config.data_flights(t)

        if json: # TODO clean this whole bit up
            graph_json = self.__data_config.data_graph_json(t)
        else:
            graph_json = None
        
        if yaml:
            graph_yaml = self.__data_config.data_graph_yaml(t)
        else:
            graph_yaml = None
        
        if npz:
            graph_npz = self.__data_config.data_graph_npz(t)
        else:
            graph_npz = None
        
        self.__airspaces.reset_result()
        self.__airspaces.process_flights_file(data_flights)

        if self.verbose:
            print("Done processing, saving as:")
            print("JSON: {}".format(graph_json))
            print("YAML: {}".format(graph_yaml))
            print("NPZ:  {}".format(graph_npz))
        
        matrix = self.__airspaces.get_result()
        
        check_file(graph_json)
        check_file(graph_yaml)
        check_file(graph_npz)
        save_graph_to_file(self.__gdf, matrix, graph_json, graph_yaml, graph_npz)

        if self.verbose:
            print("Done.")

    def process_flights_bulk(self, time_start, time_end, json=False, yaml=False, npz=True):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        execute_bulk_between(lambda t1, t2: self.process_flights(t1, json, yaml, npz), t_start, t_end)