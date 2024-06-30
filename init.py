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
import time
import numpy as np


# Import graph from file

start = time.process_time()

G = nx.read_weighted_edgelist('graphs\WikiTalk.txt', comments='#', create_using=nx.DiGraph)

# Identifying the SCCs of the graph
sccs = list(nx.strongly_connected_components(G))

# New graph created using the SCCs
scc_graph = nx.condensation(G, scc=sccs)

# Dictionary storing nodes and their correspoding SCC
node_to_scc = {}
for i, scc in enumerate(sccs):
    for node in scc:
        node_to_scc[node] = i

# PLL - 2-hop index
#vertex_order = calculate_vertex_accessing_order(scc_graph)
#L_out, L_in = pll_bfs(scc_graph, vertex_order)


# Dual Labeling
# sit_codes = assign_sit_codes(scc_graph)
# print(sit_codes)
# non_tree_edges = get_non_tree_edges(scc_graph, sit_codes)

times = []
pairs_array = np.loadtxt("pairs/random_pairs_WikiTalk.txt", dtype=str)
print("Time taken to import graph, create the SCCs and the dictionary: ", time.process_time() - start)

# for start_node, end_node in pairs_array:
#     start = time.process_time() 
#     if node_to_scc[start_node] == node_to_scc[end_node]:
#         times.append(time.process_time() - start)
#     else:
#         if dlabeling(sit_codes, non_tree_edges, node_to_scc[start_node], node_to_scc[end_node]):
#             times.append(time.process_time() - start)
#         else:
#             times.append(np.nan)


# for start_node, end_node in pairs_array:
#     start = time.process_time() 
#     #gripp(start_node, end_node, sit_codes)
#     if is_reachable_pll(L_out, L_in, node_to_scc[start_node], node_to_scc[end_node]):
#         times.append(time.process_time() - start)
#     else:
#         times.append(np.nan)

for start_node, end_node in pairs_array:
    start = time.process_time() 
    #gripp(start_node, end_node, sit_codes)
    if nx.has_path(scc_graph, node_to_scc[start_node], node_to_scc[end_node]):
        times.append(time.process_time() - start)
    else:
        times.append(np.nan)


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

print(times)
valid_times = [time if not np.isnan(time) else 0 for time in times]
print("Average time: ", sum(valid_times)/len(times))

   
# nx.draw(scc_graph, with_labels=True, node_color='skyblue', node_size=50, font_size=20, font_weight='bold')
# plt.show()

