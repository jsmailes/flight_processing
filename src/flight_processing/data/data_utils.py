from ..utils import check_file

import networkx as nx
from scipy import sparse
import pandas as pd
import geopandas

def graph_add_node(graph, name):
    if not graph.has_node(name):
        graph.add_node(name)

def graph_increment_edge(graph, u, v, amount=1):
    if graph.has_edge(u, v):
        graph[u][v]['weight'] += amount
    else:
        graph.add_edge(u, v, weight=amount)

def build_graph_from_sparse_matrix(gdf, matrix):
    n, m = matrix.shape
    assert(n == m)

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

def build_graph_from_matrix(gdf, matrix):
    n, m = matrix.shape
    assert(n == m)
    
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
    gdf_temp = gdf[gdf['name'] == name]
    if len(gdf_temp) == 0:
        return None
    if gdf_temp.iloc[0].geometry is None:
        return Point(0.0, 0.0)
    return gdf_temp.iloc[0].geometry.centroid