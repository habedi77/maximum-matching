from typing import Tuple, TypeVar, Type

import numpy as np
from abc import ABC, abstractmethod
from ..graphs.graph_base import GraphBase

G = TypeVar('G', bound=GraphBase)


class GeneratorBase(ABC):
    """
    Base class for all bipartite generators.

    All generators should specify all the parameters that can be set
    at the class level in their ``__init__`` as explicit keyword
    arguments (no ``*args`` or ``**kwargs``).
    """

    @abstractmethod
    def generate(self, size_left: int, size_right: int, graph_class: Type[G], seed: int, **kwargs) -> Tuple[G, G]:
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

    @staticmethod
    def get_kwargs_val(key: str, kwargs):
        assert key in kwargs
        value = kwargs[key]
        assert type(value) == float or type(value) == int
        return value
