import networkx as nx
from collections import defaultdict, deque

def calculate_topological_order(G):
    return list(nx.topological_sort(G))

def select_supportive_vertices(topological_order, percentage):
    total_nodes = len(topological_order)
    k = int(total_nodes * (percentage / 100))
    middle_start = total_nodes // 2 - k // 2
    middle_end = middle_start + k
    return topological_order[middle_start:middle_end]

def o_reach_bfs(G, supportive_vertices, rank):
    L_out = defaultdict(dict)
    L_in = defaultdict(dict)
    for v in supportive_vertices:
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

        # Pruning condition    
        if source in L_in[u]:  
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
        # Pruning condition
        if source in L_out[u]:  
            continue

        L_in[source][u] = d
        for neighbor in G.predecessors(u):
            if neighbor not in visited:
                queue.append((neighbor, d + 1))

def is_reachable_o_reach(G, L_out, L_in, source, target):
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


