from enum import Enum

import numpy as np
from abc import ABC, abstractmethod
from .bipartite_graph import BaseBipartiteGraph


class BaseBipartiteGenerator(ABC):
    """
    Base class for all bipartite generators.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    @abstractmethod
    def generator(self, graph: BaseBipartiteGraph, seed: int, **kwargs) -> BaseBipartiteGraph:
        """
        Generate a type of bipartite graphs

        :param graph: empty graph class of type BaseBipartiteGraph
        :param seed: seed for generator
        :param kwargs: used for additional arguments
        :return: the same BaseBipartiteGraph instance provided
        """
        pass


class GaussianBipartiteGenerator(BaseBipartiteGenerator):
    """
    bipartite graph generator based on gaussian noise.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    def generator(self, graph: BaseBipartiteGraph, seed: int, **kwargs) -> BaseBipartiteGraph:
        """
        Connect the two sets of bipartite graphs with the **left set** having an expected degree value of 'mean'

        :param graph: empty graph class of type BaseBipartiteGraph
        :param seed: seed for generator
        :param kwargs: used for additional arguments
        :key mean: Gaussian distribution mean
        :key std: Gaussian distribution std
        :return: the same BaseBipartiteGraph instance provided
        """

        assert 'mean' in kwargs
        assert 'std' in kwargs
        mean = kwargs['mean']
        std = kwargs['std']
        assert type(mean) == float or type(mean) == int
        assert type(std) == float or type(mean) == int

        size_left = graph.size_left
        size_right = graph.size_right

        degrees = np.floor(np.random.normal(loc=mean, scale=std, size=size_left))

        # bound degrees to min(0) and max(size_right)
        degrees[degrees < 0] = 0
        degrees[degrees > size_right] = size_right

        _tmp_connectivity = np.empty(size_left, dtype=object)

        for i in range(size_left):
            _tmp_connectivity[i] = np.random.choice(size_right, size=degrees[i], replace=False)
            graph.bulk_bconnect(i, _tmp_connectivity)

        return graph
