import networkx as nx
import time
import matplotlib.pyplot as plt
import sys
from collections import defaultdict, deque


def calculate_vertex_accessing_order(G):
    # Calculate the vertex accessing order based on the product of in-degree and out-degree
    degrees = [(v, (G.in_degree(v) + 1) * (G.out_degree(v) + 1)) for v in G.nodes()]
    sorted_vertices = sorted(degrees, key=lambda x: x[1], reverse=True)
    vertex_order = [v for v, d in sorted_vertices]
    return vertex_order

def select_landmarks(vertex_order, k):
    return vertex_order[:k]

def dbl_bfs(G, landmarks, rank):
    L_out = defaultdict(dict)
    L_in = defaultdict(dict)
    for v in landmarks:
        forward_bfs(G, v, rank, L_out, L_in)
        backward_bfs(G, v, rank, L_out, L_in)
    return L_out, L_in

def forward_bfs(G, source, rank, L_out, L_in):
    visited = set()
    queue = deque([(source, 0)])
    while queue:
        u, d = queue.popleft()
        if u in visited:
            continue
        visited.add(u)

        # Pruning: Skip u if it has already been processed
        if rank[u] < rank[source]:
            continue

        if source in L_in[u]:  # Pruning condition
            continue

        L_out[source][u] = d
        for neighbor in G.successors(u):
            if neighbor not in visited:
                queue.append((neighbor, d + 1))

def backward_bfs(G, source, rank, L_out, L_in):
    visited = set()
    queue = deque([(source, 0)])
    while queue:
        u, d = queue.popleft()
        if u in visited:
            continue
        visited.add(u)

        # Pruning: Skip u if it has already been processed
        if rank[u] < rank[source]:
            continue

        if source in L_out[u]:  # Pruning condition
            continue

        L_in[source][u] = d
        for neighbor in G.predecessors(u):
            if neighbor not in visited:
                queue.append((neighbor, d + 1))

def is_reachable_dbl(G, L_out, L_in, source, target):
    # Check if the target is in the L_out of the source or the source is in the L_in of the target
    if target in L_out[source] or source in L_in[target]:
        return True
    
    # Perform BFS if necessary
    return bfs_check(G, source, target)

def bfs_check(G, source, target):
    visited = set()
    queue = deque([source])
    while queue:
        u = queue.popleft()
        if u == target:
            return True
        if u in visited:
            continue
        visited.add(u)
        for neighbor in G.successors(u):
            if neighbor not in visited:
                queue.append(neighbor)
    return False