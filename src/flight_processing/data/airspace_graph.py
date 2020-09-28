from ..process_flights import AirspaceHandler
from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between, lerp
from ..scalebar import scale_bar
from .data_utils import graph_add_node, graph_increment_edge, build_graph_from_sparse_matrix, build_graph_from_matrix, get_zone_centre, save_graph_to_file, process_dataframe
from .. import config

from pathlib import Path
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
from traffic.data import opensky
from traffic.core.flight import Flight
from traffic.core.traffic import Traffic
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import logging

logger = logging.getLogger(__name__)

class AirspaceGraph:
    """
    Having constructed a graph of handovers from processing downloaded flights,
    load the graph and perform data processing on it.

    Requires a dataframe of airspaces as well as flights to have been processed using `GraphBuilder` - they must first be saved using `FlightDownloader`.

    **Summary:**

        - initialisation:
          `__init__ <#flight_processing.data.AirspaceGraph.\_\_init\_\_>`_,
          `load_graphs <#flight_processing.data.AirspaceGraph.load_graphs>`_,
          `load_graph_files <#flight_processing.data.AirspaceGraph.load_graph_files>`_
        - properties:
          `gdf <#flight_processing.data.AirspaceGraph.gdf>`_,
          `graph <#flight_processing.data.AirspaceGraph.graph>`_
        - handover testing:
          `set_confidence_values <#flight_processing.data.AirspaceGraph.set_confidence_values>`_,
          `confidence <#flight_processing.data.AirspaceGraph.confidence>`_,
          `test_point <#flight_processing.data.AirspaceGraph.test_point>`_,
          `test_handover <#flight_processing.data.AirspaceGraph.test_handover>`_,
          `test_flight <#flight_processing.data.AirspaceGraph.test_flight>`_
        - visualisation:
          `visualise_graph <#flight_processing.data.AirspaceGraph.visualise_graph>`_,
          `draw_graph_map <#flight_processing.data.AirspaceGraph.draw_graph_map>`_
        - miscellaneous:
          `get_airspace <#flight_processing.data.AirspaceGraph.get_airspace>`_,
          `airspace_distance <#flight_processing.data.AirspaceGraph.airspace_distance>`_,
          `edge_weight <#flight_processing.data.AirspaceGraph.edge_weight>`_,
          `zone_centre <#flight_processing.data.AirspaceGraph.zone_centre>`_,
          `average_edge_weight <#flight_processing.data.AirspaceGraph.average_edge_weight>`_,
          `process_single_flight <#flight_processing.data.AirspaceGraph.process_single_flight>`_
    """

    def __init__(self, dataset, df=None, dataset_location=None):
        """
        Initialise the graph builder with a given dataset, either from a file or directly from a dataframe.

        By default the dataframe will be loaded from a file as specified in the config.

        A loaded dataframe must have the following columns:
        - `name`
        - `lower_limit`
        - `upper_limit`

        In addition, a DataFrame must have a `wkt` column containing the well-known text of the airspace's geometry,
        and a GeoDataFrame must have a correctly formatted `geometry` column.

        :param dataset: dataset name or specification
        :type dataset: str or DataConfig
        :param df: dataframe of airspaces
        :type df: pandas.core.frame.DataFrame or geopandas.geodataframe.GeoDataFrame, optional
        :param dataset_location: location of saved dataframe
        :type dataset_location: pathlib.Path or str, optional

        :return: object
        :rtype: AirspaceGraph
        """

        if isinstance(dataset, DataConfig):
            self.__data_config = dataset
            self.dataset = dataset.dataset
        elif isinstance(dataset, str):
            logger.debug("Dataset argument {} is string, looking up known dataset.".format(dataset))
            self.__data_config = DataConfig.known_dataset(dataset)
            self.dataset = dataset
        else:
            raise ValueError("Argument 'dataset' must be of type DataConfig or str.")

        if df is not None:
            logger.info("Loading airspace dataset from passed in dataframe.")
            self.__gdf = process_dataframe(df)
        else:
            if dataset_location is None:
                dataset_location = self.__data_config.dataset_location

            logger.info("Loading airspace dataset from disk at location {}.".format(dataset_location))
            self.__gdf = geopandas.read_file(dataset_location)


        logger.info("Initialising AirspaceHandler C++ object.")
        self.__airspaces = AirspaceHandler()
        self.__gdf['ident'] = self.__gdf.apply(self.__add_airspace, axis=1)
        self.__gdf.set_index('ident', inplace=True)

        self.num_airspaces = self.__airspaces.size()
        logger.info("Successfully loaded airspaces, {} in total.".format(self.num_airspaces))

        self.__graph = None

        self.__distance_zero = 5000
        self.__distance_one = 3000
        self.__minimum_weight = 50
        self.__minimum_weight_adjusted = 0.05
        self.__confidence_distance = 1.0
        self.__confidence_distance_modifier = 0.8
        self.__confidence_weight = 1.0
        self.__confidence_weight_adjusted = 1.0

    @property
    def gdf(self):
        """
        Returns the underlying geopandas GeoDataFrame.

        :return: dataframe
        :rtype: geopandas.geodataframe.GeoDataFrame
        """

        return self.__gdf

    @property
    def graph(self):
        """
        Returns the underlying graph of airspace handovers.

        :return: graph
        :rtype: networkx.classes.digraph.DiGraph
        """

        return self.__graph

    def load_graphs(self, time_start, time_end):
        """
        Load the graph of handovers from a series of NPZ files within a given time range.

        Graphs will be loaded from `{data_prefix}/graphs/{dataset}/{date}/{time}.json`, where:
        - `data_prefix` is specified by the `DataConfig` object passed in on construction, or the `data_location` config value is used by default,
        - `dataset` is the name of the dataset as specified on construction,
        - `date` and `time` are determined by the timestamp.

        :param time_start: start time
        :type time_start: datetime.datetime or str
        :param time_end: end time
        :type time_end: datetime.datetime or str
        """

        logger.info("Loading matrix of handovers.")
        matrix = self.__load_npz_bulk(time_start, time_end)

        logger.info("Building graph from matrix.")
        if self.__graph is None:
            self.__graph = build_graph_from_sparse_matrix(self.__gdf, matrix)
        else:
            self.__graph = build_graph_from_sparse_matrix(self.__gdf, matrix, self.__graph)

        logger.info("Computing adjusted weights.")
        self.__graph_relative_weights()

    def load_graph_files(self, files):
        """
        Load the graph of handovers from a given list of NPZ file locations.

        :param files: file or files to load
        :type files: list(pathlib.Path) or list(str) or pathlib.Path or str
        """

        if isinstance(files, str) or isinstance(files, Path):
            to_load = [files]
        elif isinstance(files, list) and (all(isinstance(f, str) for f in files) or all(isinstance(f, Path) for f in files)):
            to_load = files
        else:
            raise ValueError("Argument 'files' must be list(pathlib.Path) or list(str) or pathlib.Path or str.")

        logger.info("Loading matrix of handovers.")
        matrix = self.__load_npz_files(to_load)

        logger.info("Building graph from matrix.")
        if self.__graph is None:
            self.__graph = build_graph_from_sparse_matrix(self.__gdf, matrix)
        else:
            self.__graph = build_graph_from_sparse_matrix(self.__gdf, matrix, self.__graph)

        logger.info("Computing adjusted weights.")
        self.__graph_relative_weights()

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

        logger.info("Loading saved graph from location {}.".format(file_load))
        return sparse.load_npz(file_load)

    def __load_npz_bulk(self, time_start, time_end):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))
        t_delta = timedelta(hours=1)
        count = math.floor((t_end - t_start) / t_delta)

        logger.info("Loading {} saved NPZ files, from {} to {}.".format(count, t_start, t_end))

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
        logger.debug("Adding airspace {} to AirspaceHandler C++ object.".format(row['name']))
        return self.__airspaces.add_airspace(row.wkt, row.lower_limit, row.upper_limit)

    def get_airspace(self, airspace):
        """
        Returns the row corresponding to the given airspace name or identifier.

        :param airspace: airspace name or identifier
        :type airspace: str or int

        :return: airspace data
        :rtype: pandas.core.series.Series
        """

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

    def airspace_distance(self, long, lat, height, airspace):
        """
        Returns the distance from the given point to the given airspace in feet.

        :param long: longitude of point
        :type long: float
        :param lat: latitude of point
        :type lat: float
        :param height: height in ft
        :type height: float
        :param airspace: airspace name or identifier
        :type airspace: str or int

        :return: distance to airspace in feet
        :rtype: float
        """

        a = self.get_airspace(airspace)

        logger.debug("Getting airspace distance using C++ AirspaceHandler object.")
        return self.__airspaces.distance_to_airspace(long, lat, height, int(a.name))

    def edge_weight(self, airspace1, airspace2):
        """
        Get the weight of the edge between the given airspaces on the graph.

        :param airspace1: first airspace name or identifier
        :type airspace1: str or int
        :param airspace2: second airspace name or identifier
        :type airspace2: str or int

        :return: edge weight
        :rtype: float
        """

        name1 = self.get_airspace(airspace1)['name']
        name2 = self.get_airspace(airspace2)['name']
        edge = self.__graph[name1].get(name2)
        if edge is not None:
            weight = edge.get('weight')
            return weight if weight is not None else 0
        else:
            return 0

    def zone_centre(self, name):
        """
        Get the centre of the given airspace.

        :param name: airspace name or identifier
        :type name: str or int

        :return: coordinates of the airspace centre
        :rtype: shapely.geometry.point.Point
        """

        return get_zone_centre(self.__gdf, self.get_airspace(name)['name'])

    def visualise_graph(self):
        """
        Visualise the graph interactively using HoloViews.
        """

        logger.info("Drawing graph using holoviews.")
        return hvnx.draw(self.__graph, mercator_positions(self.__gdf, self.__graph), edge_width=hv.dim('weight')*0.003, node_size=30, arrowhead_length=0.0001)

    def draw_graph_map(self, flight=None, subset=None, logscale=False, file_out=None):
        """
        Draw the dataframe of airspaces on a map with the graph of handovers overlaid on top, optionally plotting flights and highlighting a subset of airspaces.

        Calls pyplot's `draw` function so a diagram will be output directly.
        The result can also be saved to a file.

        :param flight: draw a flight or flights on the map
        :type flight: traffic.core.flight.Flight or traffic.core.traffic.Traffic
        :param subset: subset of airspaces to highlight (e.g. airspaces a flight passes through), as IDs or names
        :type subset: set(int) or list(int) or set(str) or list(str)
        :param logscale: edges are coloured according to a logarithmic (rather than linear) scale, default False
        :type logscale: bool
        :param file_out: save the result to a file
        :type file_out: pathlib.Path or str, optional
        """

        fig = plt.figure(dpi=300, figsize=(7,7))

        logger.info("Downloading terrain data from Stamen.")
        imagery = cimgt.Stamen(style="terrain-background")
        ax = plt.axes(projection=imagery.crs)

        ax.set_extent(self.__data_config.bounds_plt)

        ax.add_image(imagery, self.__data_config.detail)

        logger.info("Plotting airspace boundaries on map.")
        ax.add_geometries(self.__gdf.geometry, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black") #"#8fa8bf"

        logger.info("Extracting edge weights from graph.")
        _, weights_original = zip(*nx.get_edge_attributes(self.__graph, 'weight').items())
        if logscale:
            weights = tuple(map(lambda x: math.log(x), weights_original))
        else:
            weights = weights_original
        positions_transformed = mercator_positions(self.__gdf, self.__graph)
        cmap = plt.cm.Purples

        logger.info("Plotting graph on map.")
        nodes = nx.draw_networkx_nodes(self.__graph, positions_transformed, ax=ax, node_size=5, node_color="red")
        edges = nx.draw_networkx_edges(self.__graph, positions_transformed, ax=ax, node_size=5, edge_color=weights, edge_cmap=cmap, arrowsize=5, arrowstyle="->", width=0.8)
        nodes.set_zorder(20)
        for edge in edges:
            edge.set_zorder(19)

        if flight is not None:
            logger.info("Plotting flight(s) on map.")
            if isinstance(flight, Flight):
                flight.plot(ax)
            elif isinstance(flight, Traffic):
                for f in flight:
                    f.plot(ax)
            else:
                raise ValueError("Flight must be of type Flight or Traffic.")

        if subset is not None:
            logger.info("Plotting subset of airspaces on map.")
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
            logger.info("Saving figure to {}".format(file_out))
            plt.savefig(file_out, bbox_inches='tight', transparent=True)

        plt.show()

    def average_edge_weight(self, median=False):
        """
        Get the average edge weight across the whole graph.

        :param median: return median weight instead of mean, default False
        :type median: bool, optional

        :return: average edge weight
        :rtype: float
        """

        if median:
            logger.info("Computing median edge weight in graph.")

            weights = [edge[2]['weight'] for edge in list(self.__graph.edges(data=True))]
            weights.sort()

            n = len(weights)

            if n % 2 == 1:
                return weights[(n - 1) // 2]
            else:
                v1 = weights[n // 2]
                v2 = weights[(n // 2) - 1]
                return (v1 + v2) / 2
        else:
            logger.info("Computing mean edge weight in graph.")

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

    def set_confidence_values(self,
                              distance_zero=None,
                              distance_one=None,
                              minimum_weight=None,
                              minimum_weight_adjusted=None,
                              confidence_distance=None,
                              confidence_distance_modifier=None,
                              confidence_weight=None,
                              confidence_weight_adjusted=None
                              ):
        """
        Sets the confidence values used in
        `confidence <#flight_processing.data.AirspaceGraph.confidence>`_,
        `test_point <#flight_processing.data.AirspaceGraph.test_point>`_,
        `test_handover <#flight_processing.data.AirspaceGraph.test_handover>`_,
        and `test_flight <#flight_processing.data.AirspaceGraph.test_flight>`_.

        These values are set to the following by default:
        - distance_zero = 5000
        - distance_one = 3000
        - minimum_weight = 50
        - minimum_weight_adjusted = 0.05
        - confidence_distance = 1.0
        - confidence_distance_modifier = 0.8
        - confidence_weight = 1.0
        - confidence_weight_adjusted = 1.0

        These values should be modified according to data extracted from
        handovers and from the specific graph used.

        ``distance_zero`` and ``distance_one`` do not depend on the graph, but
        ``minimum_weight`` and ``minimum_weight_adjusted`` should be modified
        to fit the graph since they are based on its weights.

        It must hold that ``distance_zero >= distance_one``.

        :param distance_zero: distance from airspace border above which confidence is not increased
        :type distance_zero: float
        :param distance_one: distance from airspace border below which confidence is increased by ``confidence_distance``
        :type distance_one: float
        :param minimum_weight: minimum graph edge weight before confidence value is increased
        :type minimum_weight: float
        :param minimum_weight_adjusted: minimum "adjusted" graph edge weight before confidence value is increased - adjusted weight is the edge weight divided by the total weight of all edges leaving that node
        :type minimum_weight: float
        :param confidence_distance: if distance is sufficiently low, how much to increase confidence by
        :type confidence_distance: float
        :param confidence_distance_modifier: if aircraft is not in either airspace, multiply distance-based confidence by this value (should be ``<=1.0``)
        :type confidence_distance_modifier: float
        :param confidence_weight: if edge weight is sufficiently high, how much to increase confidence by
        :type confidence_weight: float
        :param confidence_weight_adjusted: if "adjusted" edge weight is sufficiently high, how much to increase confidence by
        :type confidence_weight_adjusted: float
        """

        if distance_zero is not None and distance_one is not None:
            assert(distance_zero >= distance_one)
            self.__distance_zero = distance_zero
            self.__distance_one = distance_one
        else:
            if distance_zero is not None:
                assert(distance_zero >= self.__distance_one)
                self.__distance_zero = distance_zero
            if distance_one is not None:
                assert(self.__distance_zero >= distance_one)
                self.__distance_one = distance_one

        if minimum_weight is not None:
            self.__minimum_weight = minimum_weight
        if minimum_weight_adjusted is not None:
            self.__minimum_weight_adjusted = minimum_weight_adjusted
        if confidence_distance is not None:
            self.__confidence_distance = confidence_distance
        if confidence_distance_modifier is not None:
            self.__confidence_distance_modifier = confidence_distance_modifier
        if confidence_weight is not None:
            self.__confidence_weight = confidence_weight
        if confidence_weight_adjusted is not None:
            self.__confidence_weight_adjusted = confidence_weight_adjusted

    def confidence(self, edge, distance1=None, distance2=None):
        """
        Given a graph edge and (optional) distance to an airspace, return information on the confidence about that handover.

        :param edge: edge from handover graph
        :type edge: dict
        :param distance1: distance to first airspace
        :type distance1: float, optional
        :param distance2: distance to second airspace
        :type distance2: float, optional

        :return: information about handover confidence
        :rtype: dict
        """

        if edge is not None:
            logger.info("Getting edge weights.")
            weight = edge.get('weight')
            weight_adjusted = edge.get('weight_adjusted')
        else:
            weight = 0
            weight_adjusted = 0

        if distance1 is not None and distance2 is not None:
            logger.info("Computing confidence based on distance from airspace borders.")
            if distance1 == 0: # aircraft inside first airspace, assume approaching second airspace
                confidence_distance = lerp(distance2, self.__distance_zero, self.__distance_one, 0.0, 1.0)
            elif distance2 == 0: # aircraft inside second airspace, assume just left first airspace
                confidence_distance = lerp(distance1, self.__distance_zero, self.__distance_one, 0.0, 1.0)
            else: # aircraft in neither airspace, check distance to second airspace but reduce confidence
                confidence_distance = lerp(distance2, self.__distance_zero, self.__distance_one, 0.0, 1.0)
                confidence_distance *= self.__confidence_distance_modifier
        else:
            confidence_distance = 0

        logger.info("Computing confidence based on non-position-based data sources.")

        confidence_weight = int(weight >= self.__minimum_weight)
        confidence_weight_adjusted = int(weight_adjusted >= self.__minimum_weight_adjusted)

        confidence_distance *= self.__confidence_distance
        confidence_weight *= self.__confidence_weight
        confidence_weight_adjusted *= self.__confidence_weight_adjusted

        confidence = confidence_distance + confidence_weight + confidence_weight_adjusted

        return dict(
            distance1 = distance1,
            distance2 = distance2,
            confidence = confidence,
            weight = weight,
            weight_adjusted = weight_adjusted,
            confidence_distance = confidence_distance,
            confidence_weight = confidence_weight,
            confidence_weight_adjusted = confidence_weight_adjusted
        )

    def process_single_flight(self, flight):
        """
        Process a single flight, returning an ordered list of airspace handovers.

        :param flight: flight to process
        :type flight: traffic.core.flight.Flight

        :return: list of handovers as pairs of identifiers
        :rtype: list(list(int))
        """

        logger.info("Converting flight to arrays of coordinates.")
        xs = np.array([c[0] for c in list(flight.coords)])
        ys = np.array([c[1] for c in list(flight.coords)])
        hs = np.array([c[2] for c in list(flight.coords)])

        logger.info("Processing flight using AirspaceHandler C++ object.")
        return self.__airspaces.process_single_flight(xs, ys, hs)

    def test_point(self, long, lat, height):
        """
        Test a point, returning a list of potential handovers which could occur at that point and their confidence.

        For each airspace which contains the given point we return a number of airspaces near that point,
        along with the confidence value of that (potential) handover.
        This takes the form of a list of dictionaries.

        :param long: longitude of point
        :type long: float
        :param lat: latitude of point
        :type lat: float
        :param height: height in ft
        :type height: float

        :return: information about handovers
        :rtype: list(dict)
        """

        ft = True # TODO add option to allow height in metres?

        logger.info("Getting airspaces at the given point using AirspaceHandler C++ object.")
        ids_at_point = self.__airspaces.airspaces_at_point(long, lat, height, ft)
        logger.info("Getting airspaces near to the given point using AirspaceHandler C++ object.")
        near_point = self.__airspaces.airspaces_near_point(long, lat, height, ft)

        out = []

        logger.info("Computing confidence in a handover to each nearby airspace.")
        for id_at in ids_at_point:
            a1 = self.__gdf.loc[id_at]
            name_at = a1['name']

            for (id_near, distance) in near_point:
                a2 = self.__gdf.loc[id_near]
                name_near = a2['name']
                edge = self.__graph[name_at].get(name_near)

                confidence = self.confidence(edge, 0.0, distance) # we know the point is within the first airspace so we set distance1 to 0.0

                confidence['airspace1'] = a1.name
                confidence['airspace2'] = a2.name
                confidence['name1'] = a1['name']
                confidence['name2'] = a2['name']

                out.append(confidence)

        return out

    def test_handover(self, long, lat, height, airspace1, airspace2):
        """
        Test a handover at a given point, returning a dictionary containing information about that handover (including confidence).

        :param long: longitude of point
        :type long: float
        :param lat: latitude of point
        :type lat: float
        :param height: height in ft
        :type height: float
        :param airspace1: first airspace name or identifier
        :type airspace1: str or int
        :param airspace2: second airspace name or identifier
        :type airspace2: str or int

        :return: information about handover
        :rtype: dict
        """

        a1 = self.get_airspace(airspace1)
        a2 = self.get_airspace(airspace2)
        if a1 is None or a2 is None:
            raise ValueError("Airspace not found!")

        edge = self.__graph[a1['name']].get(a2['name'])

        logger.debug("Getting airspace distances using C++ AirspaceHandler object.")
        distance1 = self.__airspaces.distance_to_airspace(long, lat, height, int(a1.name))
        distance2 = self.__airspaces.distance_to_airspace(long, lat, height, int(a2.name))

        logger.debug("Computing handover confidence.")
        confidence = self.confidence(edge, distance1, distance2)

        return confidence

    def test_flight(self, flight):
        """
        Test a given flight, returning each of the handovers that could have occurred during the flight and information about that handover's confidence.

        :param flight: flight to test
        :type flight: traffic.core.flight.Flight

        :return: information about handovers
        :rtype: list(dict)
        """

        if not isinstance(flight, Flight):
            raise ValueError("Argument must be of type Flight!")

        logger.info("Getting all handovers along the flight.")
        handovers = self.process_single_flight(flight)

        out = []

        logger.info("Computing confidence values for each handover.")
        for airspace1, airspace2 in handovers:
            a1 = self.get_airspace(airspace1)
            a2 = self.get_airspace(airspace2)

            edge = self.__graph[a1['name']].get(a2['name'])

            confidence = self.confidence(edge)

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
    """
    Convert a point from the WGS84 coordinate system to Mercator.

    :param point: point to convert
    :type point: shapely.geometry.point.Point

    :return: converted point
    :rtype: shapely.geometry.point.Point
    """

    return transform(wgs84_to_mercator, point)

def mercator_positions(gdf, graph):
    """
    For a given dataframe and graph, get a list of coordinates of airspace centres for each node in the graph according to the Mercator coordinate system.

    :param gdf: dataframe to use
    :type gdf: geopandas.geodataframe.GeoDataFrame
    :param graph: graph to use
    :type graph: networkx.classes.digraph.DiGraph

    :return: list of coordinates
    :rtype: list(list(float))
    """

    logger.debug("Getting the coordinates of the centre of each airspace in the Mercator projection.")

    positions_transformed = dict()
    for name in list(nx.nodes(graph)):
        positions_transformed[name] = list(point_to_mercator(get_zone_centre(gdf, name)).coords)[0]
    return positions_transformed
