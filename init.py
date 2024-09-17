import networkx as nx
import matplotlib.pyplot as plt
from scc_lookup import in_same_scc
from algorithms.dfs import dfs
from algorithms.bfs import bfs
from algorithms.gripps import assign_sit_codes, gripp
from algorithms.dlabeling import assign_sit_codes, dlabeling, get_non_tree_edges
from algorithms.create_tc import tc
from random_pairs_generator import random_pairs
from algorithms.pll import calculate_vertex_accessing_order, pll_bfs, is_reachable_pll
from algorithms.dbl import select_landmarks, dbl_bfs, is_reachable_dbl
from algorithms.oreach import calculate_topological_order, select_supportive_vertices, is_reachable_o_reach, o_reach_bfs
import time
import numpy as np


# Import graph from file
G = nx.read_edgelist('graphs_snap\web-Stanford.txt', comments='%', create_using=nx.DiGraph)
pairs_array = np.loadtxt('pairs_snap/random_pairs_web-stanford.txt', dtype=str)

start = time.process_time()
# Identifying the SCCs of the graph
sccs = list(nx.strongly_connected_components(G))

# New graph created using the SCCs
scc_graph = nx.condensation(G, scc=sccs)

# Dictionary storing nodes and their correspoding SCC
node_to_scc = {}
for i, scc in enumerate(sccs):
    for node in scc:
        node_to_scc[node] = i

# Partial 2-hop index
# percentage = 30  # 30%
# k = int(len(scc_graph.nodes()) * (percentage / 100))
# vertex_order = calculate_vertex_accessing_order(scc_graph)
# landmarks = select_landmarks(vertex_order, k)
# rank = {v: i for i, v in enumerate(vertex_order)}
# L_out, L_in = dbl_bfs(scc_graph, landmarks, rank)

# PLL - 2-hop index
# vertex_order = calculate_vertex_accessing_order(G)
# L_out, L_in = pll_bfs(G, vertex_order)

# O' Reach
topological_order = calculate_topological_order(scc_graph)
percentage = 30  # 30%
supportive_vertices = select_supportive_vertices(topological_order, percentage)
vertex_order = calculate_vertex_accessing_order(scc_graph)
rank = {v: i for i, v in enumerate(vertex_order)}
L_out, L_in = o_reach_bfs(scc_graph, supportive_vertices, rank)


# Dual Labeling
# sit_codes = assign_sit_codes(scc_graph)
# non_tree_edges = get_non_tree_edges(scc_graph, sit_codes)

print("Index construction time: ", time.process_time() - start)

total_time = time.process_time()
times = []
for start_node, end_node in pairs_array:
    if node_to_scc[start_node] == node_to_scc[end_node]:
        times.append(1)
    else:
        if is_reachable_o_reach(scc_graph, L_out, L_in, node_to_scc[start_node], node_to_scc[end_node]):
            times.append(2)
        else:
            times.append(np.nan)

print("Total time to run 1000 queries: ", time.process_time() - total_time)
#print(times)

# for start_node, end_node in pairs_array:
#     start = time.process_time() 
#     if is_reachable_dbl(scc_graph, L_out, L_in, node_to_scc[start_node], node_to_scc[end_node]):
#         times.append(time.process_time() - start)
#     else:
#         times.append(np.nan)



# for start_node, end_node in pairs_array:
#     if node_to_scc[start_node] == node_to_scc[end_node]:
#         times.append(1)
#     else:
#         if nx.has_path(scc_graph, node_to_scc[start_node], node_to_scc[end_node]):
#             times.append(2)
#         else:
#             times.append(np.nan)


#     If tc.csv is not created, run this command
# tc(scc_graph)
# print("Time taken to import graph, create the SCCs, the dictionary and the TC: ", time.process_time() - start)
   
# tc_matrix = np.loadtxt('tc.csv', delimiter=',')
# for start_node, end_node in pairs_array:
#     start = time.process_time()
#     if tc_matrix[node_to_scc[start_node], node_to_scc[end_node]] == 1:
#         times.append(time.process_time() - start)
#     else:
#         times.append(np.nan)


   
# nx.draw(scc_graph, with_labels=True, node_color='skyblue', node_size=50, font_size=20, font_weight='bold')
# plt.show()

