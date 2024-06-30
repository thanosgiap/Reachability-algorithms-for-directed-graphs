import networkx as nx
import time

def dfs(G, start_node, end_node, visited=None):

    if visited is None:
        visited = set()
    
    visited.add(start_node)

    if start_node == end_node:
        return True
    
    for neighbor in G.neighbors(start_node):
        if neighbor not in visited:
            if dfs(G, neighbor, end_node, visited):
                return True
    
   
    return False