from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between
from ..process_flights import version, AirspaceHandler
from ..scalebar import scale_bar
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre, save_graph_to_file, process_dataframe

from datetime import datetime, timedelta
from dateutil import parser
from scipy import sparse
import pandas as pd
import numpy as np
import geopandas
from shapely.geometry import Point
import shapely.wkt
import tempfile, os
from traffic.core.flight import Flight
from traffic.core.traffic import Traffic
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

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
            print("Loading airspace data from {}.".format(dataset_location))
        self.__gdf = geopandas.read_file(dataset_location)

        self.__airspaces = AirspaceHandler()

        if self.verbose:
            print("Adding airspace data to C++.")
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)

    @classmethod
    def from_dataframe(cls, dataset, df, verbose=False):
        if verbose:
            print("Preprocessing dataframe...")

        gdf = process_dataframe(df)

        fd, path = tempfile.mkstemp(suffix='.json')

        if verbose:
            print("Saving dataframe to temporary file at {}...".format(path))

        gdf.to_file(path, driver="GeoJSON")

        out = cls(dataset, verbose=verbose, dataset_location=path)

        if verbose:
            print("Removing temporary file at {}...".format(path))

        os.remove(path)

        return out

    def process_single_flight(self, flight):
        xs = np.array([c[0] for c in list(flight.coords)])
        ys = np.array([c[1] for c in list(flight.coords)])
        hs = np.array([c[2] for c in list(flight.coords)])
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

    def process_flights_bulk(self, time_start, time_end, npz=True, json=False, yaml=False):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        execute_bulk_between(lambda t1, t2: self.process_flights(t1, npz=npz, yaml=yaml, json=json), t_start, t_end)

    def draw_map(self, file_out=None, flight=None, subset=None):
        fig = plt.figure(dpi=300, figsize=(7,7))

        imagery = cimgt.Stamen(style="terrain-background")
        ax = plt.axes(projection=imagery.crs)

        ax.set_extent(self.__data_config.bounds_plt)

        ax.add_image(imagery, self.__data_config.detail)

        ax.add_geometries(self.__gdf.geometry, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black")

        if flight is not None:
            if isinstance(flight, Flight):
                flight.plot(ax)
            elif isinstance(flight, Traffic):
                for f in flight:
                    f.plot(ax)
            else:
                raise ValueError("Flight must be of type Flight or Traffic.")

        if subset is not None:
            if isinstance(subset, list) or isinstance(subset, set):
                if all(isinstance(x, int) for x in subset):
                    gdf_filtered = self.__gdf[self.__gdf.index.isin(subset)]
                elif all(isinstance(x, str) for x in subset):
                    gdf_filtered = self.__gdf[self.__gdf.name.isin(subset)]
                else:
                    raise ValueError("Subset must be list/set of indices or airspace names.")

                ax.add_geometries(gdf_filtered.geometry, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="red")
            else:
                raise ValueError("Subset of airspaces must be a list or set!")

        scale_bar(ax, (0.75, 0.05), 100)

        ax.set_aspect('auto')

        if file_out is not None:
            plt.savefig(file_out, bbox_inches='tight', transparent=True)

        plt.show()