from ..graphs.graph_base import GraphBase
from typing import Union, Tuple, Any

from abc import ABC, abstractmethod


class AlgorithmBase(ABC):
    """
    Base class for matching algorithms

    Algorithm implementations override the run class
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self, graph: GraphBase) -> Any:
        """
        Run the matching algorithm on the given graph

        :param graph: a graph instance from the BaseBipartiteGraph abstract
        :return: TODO
        """
        pass
