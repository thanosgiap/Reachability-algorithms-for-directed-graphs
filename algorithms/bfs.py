import networkx as nx
import time

def bfs(G, start_node, end_node):
    
    visited = set()
    queue = [start_node]

    while queue:
        node = queue.pop(0)
        if node == end_node:
            return True
        if node not in visited:
            visited.add(node)
            queue.extend(neighbor for neighbor in G.neighbors(node)
                         if neighbor not in visited)
    
    return False