import numpy as np
from abc import ABC, abstractmethod


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
