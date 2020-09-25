from ..utils import check_file

import networkx as nx
from scipy import sparse
import pandas as pd
import geopandas
import shapely.wkt
from shapely.geometry import Point

def graph_add_node(graph, name):
    """
    Add a node to a NetworkX graph if it does not already exist.

    :param graph: graph to which the node should be added
    :type graph: networkx.classes.digraph.DiGraph
    :param name: name of node to be added
    :type name: str
    """
    if not graph.has_node(name):
        graph.add_node(name)

def graph_increment_edge(graph, u, v, amount=1):
    """
    Increment the edge between the given nodes by the given amount, adding the edge if necessary.

    :param graph: graph to which the edge should be added
    :type graph: networkx.classes.digraph.DiGraph
    :param u: name of first node
    :type u: str
    :param v: name of second node
    :type v: str
    :param amount: amount by which to increment the edge, default 1
    :type amount: int, optional
    """
    if graph.has_edge(u, v):
        graph[u][v]['weight'] += amount
    else:
        graph.add_edge(u, v, weight=amount)

def build_graph_from_sparse_matrix(gdf, matrix, graph=None):
    """
    Given a sparse matrix, construct a NetworkX graph.

    Optionally takes another graph - if this argument is used, this function will
    instead add to this graph. The graph will be edited in-place.

    :param gdf: dataframe for the airspace for which the graph is being constructed
    :type gdf: geopandas.geodataframe.GeoDataFrame
    :param matrix: sparse matrix from which to construct the graph
    :type matrix: scipy.sparse.csr.csr_matrix
    :param graph: existing graph to add to
    :type graph: networkx.classes.digraph.DiGraph, optional

    :return: graph of airspace handovers
    :rtype: networkx.classes.digraph.DiGraph
    """
    n, m = matrix.shape
    assert(n == m)

    if graph is None:
        graph = nx.DiGraph()
        for i in range(n):
            name = gdf.loc[i]['name']
            graph_add_node(graph, name)

    I, J, V = sparse.find(matrix)
    N = I.size

    for k in range(N):
        i = I[k]
        j = J[k]
        v = V[k]
        name_i = gdf.loc[i]['name']
        name_j = gdf.loc[j]['name']
        graph_increment_edge(graph, name_i, name_j, v)

    return graph

def build_graph_from_matrix(gdf, matrix, graph=None):
    """
    Given a 2D numpy array, construct a NetworkX graph.

    Optionally takes another graph - if this argument is used, this function will
    instead add to this graph. The graph will be edited in-place.

    :param gdf: dataframe for the airspace for which the graph is being constructed
    :type gdf: geopandas.geodataframe.GeoDataFrame
    :param matrix: matrix from which to construct the graph
    :type matrix: numpy.ndarray
    :param graph: existing graph to add to
    :type graph: networkx.classes.digraph.DiGraph, optional

    :return: graph of airspace handovers
    :rtype: networkx.classes.digraph.DiGraph
    """
    n, m = matrix.shape
    assert(n == m)

    if graph is None:
        graph = nx.DiGraph()
        for i in range(n):
            name = gdf.loc[i]['name']
            graph_add_node(graph, name)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                name_i = gdf.loc[i]['name']
                name_j = gdf.loc[j]['name']
                graph_increment_edge(graph, name_i, name_j, matrix[i][j])

    return graph

def save_graph_to_file(gdf, matrix, graph_json=None, graph_yaml=None, graph_npz=None):
    """
    Given a graph represented as a 2D numpy array, save it to the specified files in the correct formats.

    :param gdf: dataframe for the graph's airspace
    :type gdf: geopandas.geodataframe.GeoDataFrame
    :param matrix: matrix representing the graph
    :type matrix: numpy.ndarray
    :param graph_json: location of JSON output
    :type graph_json: str, optional
    :param graph_yaml: location of YAML output
    :type graph_yaml: str, optional
    :param graph_npz: location of NPZ output
    :type graph_npz: str, optional
    """
    if graph_json is not None:
        check_file(graph_json)
        with open(graph_json, "w") as outfile:
            outfile.write(json.dumps(dict(graph=matrix.tolist()), indent=0))

    if graph_yaml is not None:
        check_file(graph_yaml)
        graph = build_graph_from_matrix(gdf, matrix) # TODO this can be done better
        nx.write_yaml(graph, graph_yaml)

    if graph_npz is not None:
        matrix_sparse = sparse.csr_matrix(matrix)
        sparse.save_npz(graph_npz, matrix_sparse)

def get_zone_centre(gdf, name):
    """
    Get the centre of the given airspace.

    :param gdf: dataframe of airspaces
    :type gdf: geopandas.geodataframe.GeoDataFrame
    :param name: airspace name
    :type name: str

    :return: coordinates of the airspace centre
    :rtype: shapely.geometry.point.Point
    """
    gdf_temp = gdf[gdf['name'] == name]
    if len(gdf_temp) == 0:
        return None
    if gdf_temp.iloc[0].geometry is None:
        return Point(0.0, 0.0)
    return gdf_temp.iloc[0].geometry.centroid

def process_dataframe(df):
    """
    Takes a DataFrame or GeoDataFrame and ensures it has the necessary columns, returning a GeoDataFrame with correctly formatted geometry columns.

    Must have the following columns:
    - `name`
    - `lower_limit`
    - `upper_limit`

    In addition, a DataFrame must have a `wkt` column containing the well-known text of the airspace's geometry,
    and a GeoDataFrame must have a correctly formatted `geometry` column.

    :param df: dataframe of airspaces
    :type df: pandas.core.frame.DataFrame or geopandas.geodataframe.GeoDataFrame

    :return: geodataframe of airspaces, correctly formatted
    :rtype: geopandas.geodataframe.GeoDataFrame
    """
    if isinstance(df, pd.DataFrame):
        df2 = df.copy()
        required_columns = {'name', 'wkt', 'lower_limit', 'upper_limit'}
        if not required_columns <= set(df2.columns):
            raise ValueError("DataFrame must contain columns 'name', 'wkt', 'lower_limit', 'upper_limit'.")
        if not 'geometry' in list(df2.columns):
            df2['geometry'] = df2.wkt.apply(shapely.wkt.loads)
        gdf = geopandas.GeoDataFrame(df2, geometry=df2.geometry)
    elif isinstance(df, geopandas.GeoDataFrame):
        df2 = df.copy()
        required_columns = {'name', 'lower_limit', 'upper_limit'}
        if not required_columns <= set(df2.columns):
            raise ValueError("GeoDataFrame must contain columns 'name', 'lower_limit', 'upper_limit'.")
        if not 'wkt' in list(df2.columns):
            df2['wkt'] = df2.geometry.apply(lambda g: g.wkt)
        gdf = df2
    else:
        raise ValueError("df must be a DataFrame or GeoDataFrame!")

    return gdf