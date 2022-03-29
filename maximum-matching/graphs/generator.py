from enum import Enum

import numpy as np
from abc import ABC, abstractmethod


class StorageType(Enum):
    FullMatrix = "full_matrix",
    BipartiteMatrix = "bipartite_matrix",
    SparseList = "sparse_list"


class BaseBipartiteGenerator(ABC):
    """
    Base class for all bipartite generators.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    @abstractmethod
    def generator(self, n: int, m: int, seed: int, storage: str, **kwargs) -> np.ndarray:
        """
        Generate a type of bipartite graphs

        :param n: number of vertices in the left set
        :param m: number of vertices in the left set
        :param seed: seed for generator
        :param storage: not implemented yet
        :param kwargs: used for additional arguments
        :return: a compact adjacency matrix
        """
        pass


class GaussianBipartiteGenerator(BaseBipartiteGenerator):
    """
    bipartite graph generator based on gaussian noise.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    def generator(self, n: int, m: int, seed: int, storage: str, **kwargs) -> np.ndarray:
        """
        Generate a type of bipartite graphs

        :param n: number of vertices in the left set
        :param m: number of vertices in the left set
        :param seed: seed for generator
        :param storage: not implemented yet
        :param kwargs: used for additional arguments
        :return: a compact adjacency matrix
        """

        assert 'mean' in kwargs
        assert 'std' in kwargs
        mean = kwargs['mean']
        std = kwargs['std']
        assert type(mean) == float or type(mean) == int
        assert type(std) == float

        degrees = np.floor(np.random.normal(loc=mean, scale=std, size=n))

        # bound degrees to min(0) and max (m)
        degrees[degrees < 0] = 0
        degrees[degrees > m] = m

        basic_connectivity = np.empty(n, dtype=object)

        for i in range(n):
            basic_connectivity[i] = np.random.choice(m, size=degrees[i], replace=False)

        if storage is None or storage == StorageType.FullMatrix:
            # TODO Optimize
            size = n + m
            result = np.zeros(size, dtype=bool)
            for i in range(n):
                for j in range(m):
                    row, col = i, j + n
                    result[row, col] = result[col, row] = j in basic_connectivity[i]
        else:
            raise ValueError(f"storage value '{storage}' not supported")

        return result
