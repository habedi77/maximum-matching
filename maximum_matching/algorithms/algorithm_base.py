from ..graphs.graph_base import GraphBase
from typing import Union, Tuple, Any, List
from abc import ABC, abstractmethod


class AlgorithmBase(ABC):
    """
    Base class for matching algorithms

    Algorithm implementations override the run class
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self, graph: GraphBase, **kwargs) -> Tuple[int, Union[List, None]]:
        """
        Run the matching algorithm on the given graph

        :param graph: a graph instance from the BaseBipartiteGraph abstract
        :param kwargs: additional arguments if needed
        :return: the final matching size with a list of matching size trend for online algorithms
        """

        pass
