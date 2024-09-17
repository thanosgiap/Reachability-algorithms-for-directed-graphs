import networkx as nx
import time
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from algorithms.dfs import dfs

def assign_sit_codes(G):
    sit_codes = {}
    order = 0  
    
    for start_node in G.nodes():
        if start_node not in sit_codes:
            stack = [(start_node, iter(G.successors(start_node)))]
            while stack:
                node, successors = stack[-1]
                if node not in sit_codes:
                    sit_codes[node] = (order, None)  # Set the preorder value
                    order += 1
                try:
                    successor = next(successors)
                    if successor not in sit_codes:  
                        stack.append((successor, iter(G.successors(successor))))  # Push unvisited successors onto the stack
                except StopIteration:
                    stack.pop()  # Pop the node from the stack when all successors have been visited
                    sit_codes[node] = (sit_codes[node][0], order)  # Set the postorder value
                    order += 1

    return sit_codes


def gripp(start_node, end_node, sit_codes, scc_graph):

    start_sit = sit_codes[start_node]
    end_sit = sit_codes[end_node]

    if start_sit[0] < end_sit[0] and end_sit[1] < start_sit[1]:
        return True
    else:
        return dfs(scc_graph, start_node, end_node)