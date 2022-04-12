from random import shuffle
from typing import Any

from ..graphs.graph_base import *
from .algorithm_base import AlgorithmBase


class Vazirani(AlgorithmBase):

    def run(self, graph: BaseGraph) -> Any:
        """
        Run Vazirani algorithm
        Based on https://people.eecs.berkeley.edu/~vazirani/pubs/online.pdf
        Given a bipartite graph G(U,V,E)

        Assumption: Graphs are not necessarily complete [Contrary to the paper]
        Let V = girls, U = boys, where U represents rows of an nxn matrix to vertices in U
        Or in other words, boys and girls are two disjoint sets defined in a bipartite graph

        :param graph: a graph instance from the BaseBipartiteGraph abstract
        :return: TODO
        """
        # Assumption: Boys arrive first [left = boys, right = girls]
        boys = graph.b_get_independent_set(left_set=BipartiteSet.left)

        if len(boys) == 0:
            raise ValueError("The left set of the graph is empty")

        # Priority is given to boys through their order in the array
        shuffle(boys)

        # Complete when there are no more vertices
        # Get the next vertex from the girls set

        print("running Vazirani ... ")

        next_v_right = 0
        while next_v_right < graph.size_right:
            next_v_right += 1

            # TODO incomplete

        return