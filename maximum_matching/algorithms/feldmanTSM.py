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
        _, _, capacity = maxFlow.find_max_bipartite_with_cap(historicGraph, sourceSinkCap=2)

        vec = [None] * historicGraph.size

        # Find the edges from A to B of non-zero (must be unit) flow.
        for u in historicGraph.get_independent_set(BipartiteSet.left):
            for v in historicGraph.list(u):

                if capacity[u][v] == 0:  # capacity zero means flow is 1
                    if vec[u] is None:
                        vec[u] = []

                    if vec[v] is None:
                        vec[v] = []
                    
                    vec[u].append(v)
                    vec[v].append(u)

                # elif capacity[u][v] > 1:
                #     raise ValueError('Capacity should not be more than 1!')

        return vec

    def run_red_blue(self, right_size: int, vec: List, total_size: int) -> Tuple[List[int], List[int]]:
        red = [-1] * total_size
        blue = [-1] * total_size
        pred = [-1] * total_size

        for i in range(total_size):
            if vec[i] is None:
                vec[i] = []

        left_size = total_size - right_size

        for i in range(left_size, total_size):
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
                        if cur >= total_size:
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
                        if cur >= total_size:
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

    def get_type(self, size: int, right_size: int) -> Union[int, ndarray]:
        rand = np.random.randint(low=size - right_size, high=size, size=right_size)
        result = [size + size] * size

        idx = size - right_size
        for i in rand:
            result[idx] = i
            idx += 1

        return result

    def run(self, graph: GraphBase, **kwargs) -> Tuple[int, Union[List, None]]:
        assert "historic_graph" in kwargs
        historic_graph = kwargs["historic_graph"]
        assert isinstance(historic_graph, GraphBase)

        vec = self.run_max_flow(historicGraph=historic_graph)
        (red, blue) = self.run_red_blue(historic_graph.size_right, vec, historic_graph.size)
        types = self.get_type(historic_graph.size, historic_graph.size_right)

        matching_count = 0
        trends = []
        visited_nodes = 0

        visited_nodes += graph.size_left
        trends.append([visited_nodes, matching_count])

        result = [-1] * historic_graph.size
        count = [0] * historic_graph.size

        visited = set()
        for tempI in graph.b_get_independent_set(BipartiteSet.right):
            visited_nodes += 1

            neighbours = list((set(graph.b_list(tempI, False))) - visited)

            if len(neighbours) > 0:
                random_id = np.random.randint(0, len(neighbours))
                random_neighbour = neighbours[random_id]
                visited.add(random_neighbour)

                i = tempI + historic_graph.size_left

                count[types[i]] += 1
                if count[types[i]] == 1 and blue[types[i]] != -1:
                    if result[i] == -1:
                        matching_count += 1

                    result[i] = 0
                elif count[types[i]] == 2 and red[types[i]] != -1:
                    if result[i] == -1:
                        matching_count += 1

                    result[i] = 0
        
            trends.append([visited_nodes, matching_count])

        # print("matching_count: ", matching_count)

        return matching_count, trends
