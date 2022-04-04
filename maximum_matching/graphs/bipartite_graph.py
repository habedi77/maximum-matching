from typing import Union, Tuple

import numpy as np
from abc import ABC, abstractmethod


class BaseBipartiteGraph(ABC):
    """
    Base class for bipartite graphs.

    All subclasses should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    def __init__(self, size_left: int, size_right: int) -> None:
        self.size = size_left + size_right
        self.size_left = size_left
        self.size_right = size_right
        pass

    def __getitem__(self, key: Union[int, Tuple[int, int]]) -> Union[bool, np.ndarray]:
        """
        For one input returns list of connected vertices to the given vertex
        For two inputs returns whether the two vertices are connected
        :param key: index of one vertex or tuple index of two vertices
        :return: list of connected vertices or True/False if two vertices are connected
        """
        if type(key) == int:
            return self.list(key)
        elif type(key) == tuple and len(key) == 2 and type(key[0]) == int and type(key[1]) == int:
            self.connected(key[0], key[1])
        else:
            raise TypeError('index ' + str(key) + ' must be int or a tuple with two ints')

    @abstractmethod
    def list(self, i: int) -> np.ndarray:
        """
        get list of vertices connected to vertex i

        :param i: vertex index
        :return: np.ndarray of vertex indices connected to i
        """
        pass

    @abstractmethod
    def connected(self, i: int, j: int) -> bool:
        """
        Check whether vertices i and j are connected or not

        :param i: vertex index
        :param j: vertex index
        :return: True if vertices i and j are connected, False otherwise
        """
        pass

    @abstractmethod
    def blist(self, x: int, left_set: bool) -> np.ndarray:
        """
        get list of vertices connected to vertex x in the specified set

        :param left_set: whether x belongs in the left set or the right set
        :param x: vertex index in specified set
        :return: np.ndarray of vertex indices of the other set connected to x
        """
        pass

    @abstractmethod
    def bconnected(self, left: int, right: int) -> bool:
        """
        Check whether vertex form the left set is connected to the vertex from the right set

        :param left: vertex index in the left set
        :param right: vertex index in the right set
        :return: True if vertices are connected, False otherwise
        """
        pass

    @abstractmethod
    def bulk_connect(self, i: int, js: np.ndarray) -> None:
        """
        Connect vertex i to js vertices

        :param i: vertex index
        :param js: array of vertex indices to connect to
        :return: None
        """
        pass

    @abstractmethod
    def bulk_bconnect(self, left: int, rights: np.ndarray) -> None:
        """
        Connect vertex of the left set to the vertices of the right set

        :param left: vertex index in the left set
        :param rights: array of vertex indices in the right set
        :return: None
        """
        pass


class FullMatrixBipartiteGraph(BaseBipartiteGraph):
    """
    Graph class for storing adjacency matrix in a full 2D matrix.

    The left set of the graph is represented by indices 0 ~ size_left-1
    While the right set is represented by indices size_left ~ size_left+size_right-1
    """

    def __init__(self, size_left: int, size_right: int) -> None:
        super().__init__(size_left=size_left, size_right=size_right)
        self.matrix = np.zeros((self.size, self.size), dtype=bool)

    def list(self, i: int) -> np.ndarray:
        return np.where(self.matrix[i, :])[0]

    def connected(self, i: int, j: int) -> bool:
        return self.matrix[i, j]

    def bulk_connect(self, i: int, js: np.ndarray) -> None:
        self.matrix[i, js] = True

    def blist(self, x: int, left_set: bool) -> np.ndarray:
        if left_set:
            return np.where(self.matrix[x, :])[0] - self.size_left
        else:
            return np.where(self.matrix[x + self.size_left, :])[0]

    def bconnected(self, left: int, right: int) -> bool:
        return self.matrix[left, right + self.size_left]

    def bulk_bconnect(self, left: int, rights: np.ndarray) -> None:
        self.matrix[left, rights + self.size_left] = True
        self.matrix[rights + self.size_left, left] = True
