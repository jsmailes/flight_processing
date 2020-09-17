from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between
from ..process_flights import version, AirspaceHandler
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre, save_graph_to_file

from datetime import datetime, timedelta
from dateutil import parser
from scipy import sparse
import pandas as pd
import geopandas
from shapely.geometry import Point
import shapely.wkt
import tempfile, os

import networkx as nx

class GraphBuilder:
    def __add_airspace(self, row):
        return self.__airspaces.add_airspace(row.wkt, row.lower_limit, row.upper_limit)

    def __init__(self, dataset, verbose=False, dataset_location=None):
        if isinstance(dataset, DataConfig):
            self.__data_config = dataset
            self.dataset = dataset.dataset
        elif isinstance(dataset, str):
            self.__data_config = DataConfig.known_dataset(dataset)
            self.dataset = dataset
        else:
            raise ValueError("Argument 'dataset' must be of type DataConfig or str.")

        self.verbose = verbose

        if dataset_location is None:
            dataset_location = self.__data_config.dataset_location

        if self.verbose:
            print("Loading airspace data from {}.".format(dataset_location)
        self.__gdf = geopandas.read_file(dataset_location)

        self.__airspaces = AirspaceHandler()

        if self.verbose:
            print("Adding airspace data to C++.")
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)

    @classmethod
    def from_dataframe(cls, dataset, df, verbose=False):
        if verbose:
            print("Preprocessing dataframe...")

        if isinstance(df, pd.DataFrame):
            df2 = df.copy()
            required_columns = {'wkt', 'lower_limit', 'upper_limit'}
            if not required_columns <= set(df2.columns):
                raise ValueError("DataFrame must contain columns 'wkt', 'lower_limit', 'upper_limit'.")
            if not 'geometry' in list(df2.columns):
                df2['geometry'] = df2.wkt.apply(shapely.wkt.loads)
            gdf = geopandas.GeoDataFrame(df2, geometry=df2.geometry)
        elif isinstance(df, geopandas.GeoDataFrame):
            df2 = df.copy()
            required_columns = {'lower_limit', 'upper_limit'}
            if not required_columns <= set(df2.columns):
                raise ValueError("GeoDataFrame must contain columns 'lower_limit', 'upper_limit'.")
            if not 'wkt' in list(df2.columns):
                df2['wkt'] = df2.geometry.apply(lambda g: g.wkt)
            gdf = df2
        else:
            raise ValueError("df must be a DataFrame or GeoDataFrame!")

        fd, path = tempfile.mkstemp()

        if verbose:
            print("Saving dataframe to temporary file at {}...".format(path))

        gdf.to_file(path, driver="GeoJSON")

        out = cls(dataset, verbose=verbose, dataset_location=path)

        if verbose:
            print("Removing temporary file at {}...".format(path))

        os.remove(path)

        return out

    def process_single_flight(self, xs, ys, hs):
        return self.__airspaces.process_single_flight(xs, ys, hs)

    def process_flights(self, time, npz=True, json=False, yaml=False):
        t = parser.parse(str(time))

        if self.verbose:
            print("Processing data for {}.".format(t))

        data_flights = self.__data_config.data_flights(t)

        graph_npz = self.__data_config.data_graph_npz(t) if npz else None
        graph_json = self.__data_config.data_graph_json(t) if json else None
        graph_yaml = self.__data_config.data_graph_yaml(t) if yaml else None

        self.__airspaces.reset_result()
        self.__airspaces.process_flights_file(data_flights)

        if self.verbose:
            print("Done processing, saving as:")
            print("NPZ:  {}".format(graph_npz))
            print("JSON: {}".format(graph_json))
            print("YAML: {}".format(graph_yaml))

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