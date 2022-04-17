from typing import List, Tuple, Union
from maximum_matching.algorithms.algorithm_base import AlgorithmBase
from maximum_matching.graphs.graph_base import GraphBase


class FeldmanTSM(AlgorithmBase):
    """
        Create a source node s and sink node t.
        Add new edges from s to a (a are nodes of A) with weight 2.
        Orient all the edges of A to B with weight 1.
        Add new edges from b (b are nodes of B) to t with weight 2.
        Run max flow.

        Find the edges from A to B of non-zero (must be unit) flow.
        Assign red and blue color to these edges using certain conditions.

        Assign types of each nodes of B at uniformly at random.

        Now, process the online nodes. When an online node of B comes, let it be b`.
        Pick a neighbour of b` at random. Let it be a`.
        Find the type of b` let it be t`. 
        If t` arrives for the first time, and if it has blue edges then set the edge to a` as blue.
        If t` arrives for the second time, and if it has red edges then set the edge to a` as red.
        Otherwise, ignore.
    """

    def runMaxFlow():
        pass

    def runRedBlue():
        pass

    def runOnline():
        pass

    def run(self, graph: GraphBase, historicGraph: GraphBase) -> Tuple[int, Union[List, None]]:
        print("Hello TSM!")
        return (0, [0, 0])