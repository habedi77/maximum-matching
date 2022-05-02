import random
from random import shuffle
from typing import Tuple, Union, List

from ..utility.Flags import *
from .Matching import *
from .algorithm_base import AlgorithmBase
from ..graphs.graph_base import BipartiteSet


class Rand(AlgorithmBase):
    def __init__(self) -> None:
        pass

    """
    Randomized online bipartite algorithm
    As a vertex arrives, match with a random edge
    """
    def run(self, graph) -> Tuple[int, Union[List, None]]:
        # Assumption: left arrive first [left, right = the bipartite graph G = {L, R, E}]
        left = graph.get_independent_set(BipartiteSet.left)

        if left is None or len(left) == 0:
            print("Could not evaluate graph.")
            print("One of the disjoint sets are empty.")
            exit(0)

        # print("running Randomized online algorithm ... ")

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

            # As each girl arrives, match her to the eligible boy of the highest rank
            neighbours_of_vertex = graph.list(vertex)

            # Check neighbours.
            valid_matches = []
            for neigh in neighbours_of_vertex:
                edge_test = create_edge(vertex, neigh)

                if is_valid_match(max_matching, edge_test):
                    valid_matches.append(edge_test)

            # Select a random edge from the possible choices
            if len(valid_matches) > 0:
                max_matching.append(valid_matches[random.randrange(0, len(valid_matches))])

            trend.append([len(left) + num_evaluated, len(max_matching)])
            valid_matches.clear()

        return [len(max_matching), trend]
