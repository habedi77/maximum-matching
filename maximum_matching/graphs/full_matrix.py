from .graph_base import BaseGraph, BipartiteSet
import numpy as np
from typing import Union


class FullMatrixGraph(BaseGraph):
    """
    Graph class for storing adjacency matrix in a full 2D matrix.

    The left set of the graph is represented by indices 0 ~ size_left-1
    While the right set is represented by indices size_left ~ size_left+size_right-1
    """

    def __init__(self, size_left: int, size_right: int) -> None:
        super().__init__(size_left=size_left, size_right=size_right)
        self.matrix = np.zeros((self.size, self.size), dtype=bool)

    def get_independent_set(self, left_set: Union[bool, BipartiteSet]) -> np.ndarray:
        if left_set:
            return np.arange(0, self.size_left)
        else:
            return np.arange(self.size_left, self.size_right)

    def list(self, i: int) -> np.ndarray:
        return np.where(self.matrix[i, :])[0]

    def connected(self, i: int, j: int) -> bool:
        return self.matrix[i, j]

    def bulk_connect(self, i: int, js: np.ndarray) -> None:
        self.matrix[i, js] = True
        self.matrix[js, i] = True

    def b_get_independent_set(self, left_set: Union[bool, BipartiteSet]) -> np.ndarray:
        if left_set:
            return np.arange(0, self.size_left)
        else:
            return np.arange(0, self.size_right)

    def b_list(self, x: int, left_set: bool) -> np.ndarray:
        if left_set:
            return np.where(self.matrix[x, :])[0] - self.size_left
        else:
            return np.where(self.matrix[x + self.size_left, :])[0]

    def b_connected(self, left: int, right: int) -> bool:
        return self.matrix[left, right + self.size_left]

    def b_bulk_connect(self, left: int, rights: np.ndarray) -> None:
        self.matrix[left, rights + self.size_left] = True
        self.matrix[rights + self.size_left, left] = True
