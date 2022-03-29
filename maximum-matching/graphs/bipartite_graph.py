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

    def __init__(self) -> None:
        self.size = -1
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
        :return: np.ndarray of vertices connected to i
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
