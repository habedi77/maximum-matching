from .graph_base import GraphBase, BipartiteSet
import numpy as np
from typing import Union


class FullMatrixGraph(GraphBase):
    """
    Graph class for storing adjacency matrix in a full 2D matrix.

    The left set of the graph is represented by indices 0 ~ size_left-1
    While the right set is represented by indices size_left ~ size_left+size_right-1
    """

    def __init__(self, size_left: int, size_right: int) -> None:
        super().__init__(size_left=size_left, size_right=size_right)
        self.matrix = np.zeros((self.size, self.size), dtype=int)

    def get_independent_set(self, left_set: Union[bool, BipartiteSet]) -> np.ndarray:
        if left_set:
            return np.arange(0, self.size_left)
        else:
            return np.arange(self.size_left, self.size_right)

    def list(self, i: int) -> np.ndarray:
        return np.where(self.matrix[i, :] > 0)[0]

    def connected(self, i: int, j: int) -> bool:
        return self.matrix[i, j] > 0

    def bulk_connect(self, i: int, js: np.ndarray) -> None:
        self.matrix[i, js] = 1
        self.matrix[js, i] = 1

    def b_get_independent_set(self, left_set: Union[bool, BipartiteSet]) -> np.ndarray:
        if left_set:
            return np.arange(0, self.size_left)
        else:
            return np.arange(0, self.size_right)

    def b_list(self, x: int, left_set: bool) -> np.ndarray:
        if left_set:
            return np.where(self.matrix[x, :] > 0)[0] - self.size_left
        else:
            return np.where(self.matrix[x + self.size_left, :] > 0)[0]

    def b_connected(self, left: int, right: int) -> bool:
        return self.matrix[left, right + self.size_left] > 0

    def b_bulk_connect(self, left: int, rights: np.ndarray) -> None:
        self.matrix[left, rights + self.size_left] = 1
        self.matrix[rights + self.size_left, left] = 1

    def w_list(self, i: int) -> np.ndarray:
        pass

    def w_connected(self, i: int, j: int) -> int:
        pass

    def w_bulk_connect(self, i: int, js: np.ndarray) -> None:
        pass
