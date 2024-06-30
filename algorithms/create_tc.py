import networkx as nx
import numpy as np


def tc(scc_graph):

    tc = nx.transitive_closure(scc_graph)
    tc_matrix = nx.adjacency_matrix(tc).todense()

    with open('tc.csv', 'w') as file:
        for row in tc_matrix:
            file.write(','.join(map(str, row)) + '\n')

