from typing import Tuple, Type
import numpy as np
from .generator_base import GeneratorBase, G


class GaussianGenerator(GeneratorBase):

    def get_values_from_kwargs(self, key: str, kwargs):
        assert key in kwargs
        value = kwargs[key]
        assert type(value) == float or type(value) == int
        return value

    def gen_graph(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, mean: int, std: int):
        np.random.seed(seed)

        graph = graph_class(size_left=size_left, size_right=size_right)

        degrees = np.floor(np.random.normal(loc=mean, scale=std, size=size_left)).astype(int)

        # bound degrees to min(0) and max(size_right)
        degrees[degrees < 0] = 0
        degrees[degrees > size_right] = size_right

        _tmp_connectivity = np.empty(size_left, dtype=object)

        for i in range(size_left):
            _tmp_connectivity[i] = np.random.choice(size_right, size=degrees[i], replace=False)
            graph.b_bulk_connect(i, _tmp_connectivity[i])

        return graph

    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> Tuple[G, G]:
        """
        Connect the two sets of bipartite graphs with the **left set** having an expected degree value of 'mean'

        :param size_left: size of the left bipartite set
        :param size_right: size of the right bipartite set
        :param graph_class: type of graph class with base of BaseBipartiteGraph
        :param seed: seed for generator
        :param kwargs: used for additional arguments
        :key mean: Gaussian distribution mean
        :key std: Gaussian distribution std
        :return: the same BaseBipartiteGraph instance provided
        """

        mean = self.get_values_from_kwargs('mean', kwargs)
        std = self.get_values_from_kwargs('std', kwargs)
        hist_mean = self.get_values_from_kwargs('hist_mean', kwargs)
        hist_std = self.get_values_from_kwargs('hist_std', kwargs)
        hist_seed = self.get_values_from_kwargs('hist_seed', kwargs)
        hist_multiply = self.get_values_from_kwargs('hist_multiply', kwargs)

        actual_graph = self.gen_graph(size_left, size_right, graph_class, seed, mean, std)
        hist_graph = self.gen_graph(size_left * hist_multiply, size_right * hist_multiply, graph_class, hist_seed, hist_mean, hist_std)

        return (actual_graph, hist_graph)
