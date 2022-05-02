from random import shuffle
from typing import Tuple, Union, List

import numpy as np

from ..utility.Flags import *
from .Matching import *
from .algorithm_base import AlgorithmBase
from ..graphs.graph_base import BipartiteSet


class Vaz(AlgorithmBase):
    def __init__(self) -> None:
        pass

    """
    Run Vazirani algorithm
    Based on https://people.eecs.berkeley.edu/~vazirani/pubs/online.pdf
    Given a bipartite graph G(U,V,E)
    Assumption: Graphs are not necessarily complete [Contrary to the paper]
    Let V = girls, U = boys, where U represents rows of an nxn matrix to vertices in U
    Or in other words, boys and girls are two disjoint sets defined in a bipartite graph
    Return the maximum_matching. Or well, the 'estimated' best matching.
    """

    def run(self, graph) -> Tuple[int, Union[List, None]]:
        # Assumption: Boys arrive first [left = boys, right = girls]
        boys = graph.get_independent_set(BipartiteSet.left)

        if boys is None or len(boys) == 0:
            print("Could not evaluate graph.")
            print("One of the disjoint sets are empty.")
            exit(0)

        # Priority is given to boys through their order in the array
        shuffle(boys)

        # Complete when there are no more vertices
        # Get the next vertex from the girls set

        # print("running Vazirani ... ")

        girls = graph.get_independent_set(BipartiteSet.right)

        # Randomize the order of girl vertices
        if Online_Randomize:
            shuffle(girls)

        # Array of edges in our matching
        max_matching = []
        trend = [[len(boys), 0]]
        num_girls_evaluated = 0

        for vertex in girls:
            num_girls_evaluated = num_girls_evaluated + 1

            # As each girl arrives, match her to the eligible boy of the highest rank
            neighbours_of_vertex = graph.list(vertex)

            # Check neighbours. Match with the eligible boy (if any) of the highest rank
            valid_matches = []  # Pick highest rank out of the possible valid matches
            for neigh in neighbours_of_vertex:
                edge_test = create_edge(vertex, neigh)

                if is_valid_match(max_matching, edge_test):
                    valid_matches.append([edge_test, np.where(boys == neigh)])

            highest_rank = []
            for i in valid_matches:
                if len(highest_rank) == 0 or i[1][0] < highest_rank[1]:
                    highest_rank = i

            # Use the edge to the highest ranked eligible boy
            if len(highest_rank) > 0:
                max_matching.append(highest_rank[0])

            trend.append([len(boys) + num_girls_evaluated, len(max_matching)])
            valid_matches.clear()

        return [len(max_matching), trend]
