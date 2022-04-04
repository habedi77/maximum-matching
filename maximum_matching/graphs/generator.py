from enum import Enum
from typing import TypeVar, Type

import numpy as np
from abc import ABC, abstractmethod
from .bipartite_graph import BaseBipartiteGraph

G = TypeVar('G', bound=BaseBipartiteGraph)


class BaseBipartiteGenerator(ABC):
    """
    Base class for all bipartite generators.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    @abstractmethod
    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> G:
        """
        Generate a type of bipartite graphs

        :param size_left: size of the left bipartite set
        :param size_right: size of the right bipartite set
        :param graph_class: type of graph class with base of BaseBipartiteGraph
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

    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> G:
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

        assert 'mean' in kwargs
        assert 'std' in kwargs
        mean = kwargs['mean']
        std = kwargs['std']
        assert type(mean) == float or type(mean) == int
        assert type(std) == float or type(mean) == int

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
