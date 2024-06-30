import networkx as nx

def in_same_scc(start_node, end_node, sccs):
    for scc in sccs:
        if start_node in scc and end_node in scc:
            return True
    return False