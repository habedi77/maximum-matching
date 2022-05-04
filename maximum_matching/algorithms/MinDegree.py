import math
import random
from random import shuffle
from typing import Tuple, Union, List

import numpy as np

from ..utility.Flags import *
from .algorithm_base import AlgorithmBase
from ..graphs.graph_base import BipartiteSet


class MinDeg(AlgorithmBase):
    def __init__(self) -> None:
        pass

    """ 
    Minimum_Degree online bipartite algorithm
    As a vertex arrives, match to a neighbour with the minimum degree
    """
    def run(self, graph, **kwargs) -> Tuple[int, Union[List, None]]:
        # Assumption: left arrive first [left, right = the bipartite graph G = {L, R, E}]
        left = graph.get_independent_set(BipartiteSet.left)

        if left is None or len(left) == 0:
            print("Could not evaluate graph.")
            print("One of the disjoint sets are empty.")
            exit(0)

        # print("running Minimum Degree Algorithm ... ")

        right = graph.get_independent_set(BipartiteSet.right)

        # Randomize the order of right vertices
        if Online_Randomize:
            shuffle(right)

        # Array of edges in our matching
        max_matching = np.full((graph.size, 2), fill_value=-1)
        mm_idx = 0
        trend = [[len(left), 0]]
        num_evaluated = 0

        for vertex in right:
            num_evaluated = num_evaluated + 1

            # Check neighbours of arriving vertex
            neighbours_of_vertex = graph.list(vertex)

            # Match with the eligible of the minimum degree
            selected_match = []
            selected_match_degree = math.inf
            for neigh in neighbours_of_vertex:
                edge_test = [vertex, neigh]

                # Discover minimum degree match
                if edge_test[0] in max_matching or edge_test[1] in max_matching:
                    pass
                else:
                    degree = len(graph.list(neigh))
                    if degree < selected_match_degree:
                        selected_match = edge_test
                        selected_match_degree = degree

            if not math.isinf(selected_match_degree) and len(selected_match) > 0:
                max_matching[mm_idx] = selected_match
                mm_idx += 1

            trend.append([len(left) + num_evaluated, mm_idx])

        return mm_idx, trend
