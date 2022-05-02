from typing import TypeVar, Type
import numpy as np
from .generator_base import GeneratorBase, G


class DensityGenerator(GeneratorBase):

    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> G:
        """
        Connects a given percentage of edges between the two sets of a bipartite graph
        Density=0 : empty graph, Density=1 : complete bipartite graph
        Number of edges will not exceed density*size_left*size_right

        :param size_left: size of the left bipartite set
        :param size_right: size of the right bipartite set
        :param graph_class: type of graph class with base of BaseBipartiteGraph
        :param seed: seed for generator
        :param kwargs: used for additional arguments
        :key density: percentage of edges to create
        :return: populated instance of a graph_class provided
        """

        assert 'density' in kwargs
        density = kwargs['density']
        assert type(density) == float or type(density) == int
        assert 1 >= density >= 0

        np.random.seed(seed)
        graph = graph_class(size_left=size_left, size_right=size_right)

        # Distribute edges id into vertices
        edge_dist = np.random.choice(size_right * size_left, size=size_right * size_left, replace=False)
        edge_dist = edge_dist.reshape((size_left, size_right))

        # Only want ids from 0 to edge_cutoff-1
        # degrees is number of edges per vertex
        edge_cutoff = np.floor(size_left * size_right * density)
        degree = (edge_dist < edge_cutoff).sum(axis=1)

        for i in range(size_left):
            connection_index = np.random.choice(size_right, size=degree[i], replace=False)
            graph.b_bulk_connect(i, connection_index)

        return graph
