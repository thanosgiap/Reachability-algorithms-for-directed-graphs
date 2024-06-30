import networkx as nx
import time
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

def assign_sit_codes(G):
    sit_codes = {}
    order = 0  
    
    for start_node in G.nodes():
        if start_node not in sit_codes:
            stack = [(start_node, iter(G.successors(start_node)))]
            while stack:
                node, successors = stack[-1]
                if node not in sit_codes:
                    sit_codes[node] = (order, None)  
                    order += 1
                try:
                    successor = next(successors)
                    if successor not in sit_codes:  
                        stack.append((successor, iter(G.successors(successor))))  
                except StopIteration:
                    stack.pop()  
                    sit_codes[node] = (sit_codes[node][0], order)  
                    order += 1

    return sit_codes


def get_non_tree_edges(G, sit_codes):
    non_tree_edges = {}
    
    # Check whether u and v are connected via non-tree edge
    for u, v, edge_type in nx.dfs_labeled_edges(G):
        if edge_type == 'nontree':
            if u in sit_codes and v in sit_codes:
                u_preorder = sit_codes[u][0]
                v_preorder, v_postorder = sit_codes[v]
                if u_preorder not in non_tree_edges:
                    non_tree_edges[u_preorder] = []
                non_tree_edges[u_preorder].append((v_preorder, v_postorder))
            else:
                print(f"Warning: Node {u} or {v} is not in sit_codes")

    return non_tree_edges

def transitive_link_count(non_tree_edges, x, y):
    count = 0
    for i in non_tree_edges:
        if i >= x:
            for j, k in non_tree_edges[i]:
                if j <= y < k:
                    count += 1
    return count


def predicate_dg(sit_codes, non_tree_edges, u, v):
    u_start, u_end = sit_codes[u]
    v_start, _ = sit_codes[v]
    
    N_u_start_v_start = transitive_link_count(non_tree_edges, u_start, v_start)
    N_u_end_v_start = transitive_link_count(non_tree_edges, u_end, v_start)
    
    return N_u_start_v_start - N_u_end_v_start > 0

def dlabeling(sit_codes, non_tree_edges, u, v):
    u_start, u_end = sit_codes[u]
    v_start, v_end = sit_codes[v]
    
    # Tree edge condition
    if u_start <= v_start and v_start < u_end:
        return True
    
    # Non-tree edge condition
    if predicate_dg(sit_codes, non_tree_edges, u, v):
        return True
    
    return False