from ..graphs.bipartite_graph import BaseGraph
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
    def run(self, graph: BaseGraph) -> Any:
        """
        Run the matching algorithm on the given graph

        :param graph: a graph instance from the BaseBipartiteGraph abstract
        :return: TODO
        """
        pass
