from typing import List, Tuple, Union

import numpy as np
from numpy import ndarray

from maximum_matching.algorithms.algorithm_base import AlgorithmBase
from maximum_matching.algorithms.max_flow import MaxFlow
from maximum_matching.graphs.graph_base import BipartiteSet, GraphBase


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

    def run_max_flow(self, historicGraph: GraphBase) -> List:

        maxFlow = MaxFlow()
        maxFlow.find_max_bipartite(historicGraph, True, sourceSinkCap=2)

        vec = [None] * historicGraph.size

        # Find the edges from A to B of non-zero (must be unit) flow.
        for u in historicGraph.get_independent_set(BipartiteSet.left):
            for v in historicGraph.list(u):

                if maxFlow.capacity[u][v] == 0:  # capacity zero means flow is 1
                    if vec[u] is None:
                        vec[u] = []

                    if vec[v] is None:
                        vec[v] = []

                    vec[u].append(v)
                    vec[v].append(u)

                elif maxFlow.capacity[u][v] > 1:
                    raise ValueError('Capacity should not be more than 1!')

        return vec

    def run_red_blue(self, left_size: int, vec: List, total_size: int) -> Tuple[List[int], List[int]]:
        red = [-1] * left_size
        blue = [-1] * left_size
        pred = [-1] * total_size

        for i in range(left_size):
            if vec[i] is None:
                vec[i] = []

        for i in range(0, left_size):
            if pred[i] == -1 and len(vec[i]) != 0:
                cur = vec[i][0]
                pred[cur] = i
                cur_len = 2

                while len(vec[cur]) == 2 and cur != i:
                    next = -1
                    if vec[cur][0] == pred[cur]:
                        next = vec[cur][1]
                    else:
                        next = vec[cur][0]

                    pred[next] = cur
                    cur = next
                    cur_len += 1

                if cur == i:  # cycle
                    st = i
                    blue[st] = pred[st]
                    red[pred[pred[st]]] = pred[st]
                    st = pred[pred[st]]

                    while st != i:
                        blue[st] = pred[st]
                        red[pred[pred[st]]] = pred[st]
                        st = pred[pred[st]]
                else:
                    # go down the other branch
                    if len(vec[i]) == 2:
                        prev = i
                        ncur = vec[i][1]
                        pred[prev] = ncur
                        cur_len += 1

                        while len(vec[ncur]) == 2:
                            next = -1
                            if vec[ncur][0] == prev:
                                next = vec[ncur][1]
                            else:
                                next = vec[ncur][0]
                            pred[ncur] = next
                            prev = ncur
                            ncur = next
                            cur_len += 1

                        pred[ncur] = ncur
                    else:
                        pred[i] = i

                    if cur_len % 2 == 0:  # number of nodes on the path is even, i.e. length is odd
                        if cur >= left_size:
                            blue[pred[cur]] = cur
                            st = pred[cur]
                            while pred[st] != st:
                                red[st] = pred[st]
                                blue[pred[pred[st]]] = pred[st]
                                st = pred[pred[st]]

                        else:
                            blue[cur] = pred[cur]
                            st = pred[cur]
                            while pred[st] != st:
                                red[pred[st]] = st
                                blue[pred[st]] = pred[pred[st]]
                                st = pred[pred[st]]
                    else:
                        if cur >= left_size:
                            st = cur

                            blue[pred[st]] = st
                            red[pred[st]] = pred[pred[st]]
                            st = pred[pred[st]]

                            while pred[st] != st:
                                blue[pred[st]] = st
                                red[pred[st]] = pred[pred[st]]
                                st = pred[pred[st]]
                        else:
                            st = cur
                            blue[st] = pred[st]
                            blue[pred[pred[st]]] = pred[st]
                            st = pred[pred[st]]
                            while pred[st] != st:
                                red[st] = pred[st]
                                blue[pred[pred[st]]] = pred[st]
                                st = pred[pred[st]]

        return red, blue

    def get_type(self, size: int) -> Union[int, ndarray]:
        return np.random.randint(low=0, high=size, size=size)

    def run(self, graph: GraphBase, **kwargs) -> Tuple[int, Union[List, None]]:
        assert "historic_graph" in kwargs
        historic_graph = kwargs["historic_graph"]
        assert isinstance(historic_graph, GraphBase)

        vec = self.run_max_flow(historicGraph=historic_graph)
        (red, blue) = self.run_red_blue(historic_graph.size_right, vec, historic_graph.size)
        types = self.get_type(historic_graph.size_right)

        matching_count = 0
        trends = []
        visited_nodes = 0

        visited_nodes += graph.size_left
        trends.append([visited_nodes, matching_count])

        result = [-1] * historic_graph.size_right
        offline = [-1] * historic_graph.size
        count = [0] * historic_graph.size_right

        # TODO: Handle the online edge cases and update the comments
        maxFlow = MaxFlow()
        res = maxFlow.find_max_bipartite(graph, True, sourceSinkCap=1)
        for i in graph.b_get_independent_set(BipartiteSet.right):
            visited_nodes += 1
            count[types[i]] += 1
            if count[types[i]] == 1 and blue[types[i]] != -1 and offline[blue[types[i]]] == -1:
                if result[i] == -1 and matching_count < res[0]:
                    matching_count += 1

                result[i] = blue[types[i]]
                offline[blue[types[i]]] = i
            elif count[types[i]] == 2 and red[types[i]] != -1 and offline[red[types[i]]] == -1:
                if result[i] == -1 and matching_count < res[0]:
                    matching_count += 1

                result[i] = red[types[i]]
                offline[red[types[i]]] = i

            trends.append([visited_nodes, matching_count])

        return matching_count, trends
