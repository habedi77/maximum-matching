import math
import random
from random import shuffle
from typing import Tuple, Union, List

from ..utility.Flags import *
from .Matching import *
from .algorithm_base import AlgorithmBase
from ..graphs.graph_base import BipartiteSet


class MinDeg(AlgorithmBase):
    def __init__(self) -> None:
        pass

    """ 
    Minimum_Degree online bipartite algorithm
    As a vertex arrives, match to a neighbour with the minimum degree
    """
    def run(self, graph) -> Tuple[int, Union[List, None]]:
        # Assumption: left arrive first [left, right = the bipartite graph G = {L, R, E}]
        left = graph.get_independent_set(BipartiteSet.left)

        if left is None or len(left) == 0:
            print("Could not evaluate graph.")
            print("One of the disjoint sets are empty.")
            exit(0)

        print("running Minimum Degree Algorithm ... ")

        right = graph.get_independent_set(BipartiteSet.right)

        # Randomize the order of right vertices
        if Online_Randomize:
            shuffle(right)

        # Array of edges in our matching
        max_matching = []
        trend = [[len(left), 0]]
        num_evaluated = 0

        for vertex in right:
            num_evaluated = num_evaluated + 1

            # Check neighbours of arriving vertex
            neighbours_of_vertex = graph.list(vertex)

            # Match with the eligible of the minimum degree
            selected_match = []
            selected_match_size = math.inf
            for neigh in neighbours_of_vertex:
                edge_test = create_edge(vertex, neigh)

                # Discover minimum degree match
                if is_valid_match(max_matching, edge_test):
                    num_neigh = len(graph.list(neigh))
                    if num_neigh < selected_match_size:
                        selected_match = create_edge(vertex, neigh)
                        selected_match_size = num_neigh

            if not math.isinf(selected_match_size) and len(selected_match) > 0:
                max_matching.append(selected_match)

            trend.append([len(left) + num_evaluated, len(max_matching)])

        return [len(max_matching), trend]
