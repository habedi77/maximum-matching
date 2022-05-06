from typing import TypeVar, Type, Tuple
import numpy as np
from .generator_base import GeneratorBase, G


class UniformGenerator(GeneratorBase):

    def _generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, mean: float) -> G:
        """
        Connect the two sets of bipartite graphs with the **left set** having an expected degree value of 'mean'
        Number of edges will not exceed mean*size_left

        :param size_left: size of the left bipartite set
        :param size_right: size of the right bipartite set
        :param graph_class: type of graph class with base of BaseBipartiteGraph
        :param seed: seed for generator
        :param mean: graph vertices expected degree
        :return: populated instance of a graph_class provided
        """

        np.random.seed(seed)
        graph = graph_class(size_left=size_left, size_right=size_right)

        # Distribute edges id into vertices
        edge_dist = np.random.choice(size_right * size_left, size=size_right * size_left, replace=False)
        edge_dist = edge_dist.reshape((size_left, size_right))

        # Only want ids from 0 to edge_cutoff-1
        # degrees is number of edges per vertex
        edge_cutoff = np.floor(size_left * mean)
        degrees = (edge_dist < edge_cutoff).sum(axis=1)

        for i in range(size_left):
            connection_index = np.random.choice(size_right, size=degrees[i], replace=False)
            graph.b_bulk_connect(i, connection_index)

        return graph

    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> Tuple[G, G]:
        """
        Connect the two sets of bipartite graphs with the **left set** having an expected degree value of 'mean'

        :param size_left: size of the left bipartite set
        :param size_right: size of the right bipartite set
        :param graph_class: type of graph class with base of BaseBipartiteGraph
        :param seed: seed for generator
        :param kwargs: used for additional arguments
        :key mean: expected degree of the lef vertices
        :return: the same BaseBipartiteGraph instance provided
        """

        mean = self.get_kwargs_val('mean', kwargs)

        hist_mean = self.get_kwargs_val('hist_mean', kwargs)
        hist_seed = self.get_kwargs_val('hist_seed', kwargs)
        hist_multiply = self.get_kwargs_val('hist_multiply', kwargs)

        actual_graph = self._generate(size_left, size_right, graph_class, seed, mean)

        hist_graph = self._generate(size_left * hist_multiply,
                                    size_right * hist_multiply,
                                    graph_class, hist_seed,
                                    hist_mean)

        return actual_graph, hist_graph
