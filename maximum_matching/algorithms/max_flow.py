from typing import List, Tuple, Union

import numpy as np

from maximum_matching.algorithms.algorithm_base import AlgorithmBase
from maximum_matching.graphs.graph_base import BipartiteSet, GraphBase


class MaxFlow(AlgorithmBase):
    """
    Edmonds Karp algorithm implementation of the Maximum Flow problem
    """

    INF = 1000000009

    def __init__(self) -> None:
        super().__init__()
        # self.vec = np.empty(1)  # graph on which the max flow will run
        # self.visited = np.empty(1)
        # self.capacity = np.empty(1)  # 2D array for capacity
        # self.bfs_path = np.empty(1)

    @staticmethod
    def bfs(start: int, endd: int, n: int, vec, capacity) -> Tuple[bool, np.ndarray]:
        bfs_path = np.full(shape=n, fill_value=-1)
        visited = np.full(shape=n, fill_value=False, dtype=bool)
        visited[start] = True

        que = [start]
        found = False

        while len(que) > 0 and not found:
            u = que.pop(0)

            if found:
                break

            vec_u = np.where(vec[u] > -1)[0]
            vec_u_2 = vec_u[np.logical_and(np.logical_not(visited[vec_u]), capacity[u][vec_u] > 0)]

            visited[vec_u_2] = True
            bfs_path[vec_u_2] = u
            que += list(vec_u_2)

            if endd in vec_u_2:
                found = True
                break

        return found, bfs_path

    @staticmethod
    def run_max_flow(src: int, sink: int, n: int, vec, capacity) -> int:
        max_flow = 0
        min_capacity = MaxFlow.INF

        bfs_res, bfs_path = MaxFlow.bfs(src, sink, n, vec, capacity)
        while bfs_res is True:

            x = sink
            while x != src:
                min_capacity = min(min_capacity, capacity[bfs_path[x]][x])
                x = bfs_path[x]

            x = sink
            while x != src and min_capacity != MaxFlow.INF:
                capacity[bfs_path[x]][x] -= min_capacity
                capacity[x][bfs_path[x]] += min_capacity
                x = bfs_path[x]

            max_flow += min_capacity
            min_capacity = MaxFlow.INF
            bfs_res, bfs_path = MaxFlow.bfs(src, sink, n, vec, capacity)

        return max_flow

    @staticmethod
    def find_max_bipartite(graph: GraphBase, sourceSinkCap: int = 1) -> \
            Tuple[int, Union[List, None]]:

        left_side = graph.get_independent_set(BipartiteSet.left)
        right_side = graph.get_independent_set(BipartiteSet.right)

        source_node = graph.size
        sink_node = graph.size + 1
        total_nodes = graph.size + 2

        vec = np.full(shape=(total_nodes, total_nodes), fill_value=-1, dtype=int)
        capacity = np.zeros((total_nodes, total_nodes))

        # connecting source_node with left side
        vec[source_node, left_side] = 1
        vec[left_side, source_node] = 1
        capacity[left_side, source_node] = sourceSinkCap
        capacity[source_node, left_side] = sourceSinkCap

        # connecting right_side with sink_node
        vec[sink_node, right_side] = 1
        vec[right_side, sink_node] = 1
        capacity[right_side, sink_node] = sourceSinkCap
        capacity[sink_node, right_side] = sourceSinkCap

        for v in right_side:
            neighbours = graph.list(v)
            vec[neighbours, v] = 1
            vec[v, neighbours] = 1
            capacity[v, neighbours] = sourceSinkCap
            capacity[neighbours, v] = sourceSinkCap

        max_matches = MaxFlow.run_max_flow(source_node, sink_node, total_nodes, vec, capacity)

        trends = [[graph.size, max_matches]] * (graph.size_right + 1)

        return max_matches, trends

    def run(self, graph: GraphBase, **kwargs) -> Tuple[int, Union[List, None]]:
        max_matches, trends = self.find_max_bipartite(graph)

        return max_matches, trends
