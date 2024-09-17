import networkx as nx

def dfs(G, start_node, end_node):
    visited = set()
    stack = [start_node]

    while stack:
        current_node = stack.pop()

        if current_node == end_node:
            return True

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in G.neighbors(current_node):
                if neighbor not in visited:
                    stack.append(neighbor)

    return False
