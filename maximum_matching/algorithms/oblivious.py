import random
from typing import List, Tuple, Union

from maximum_matching.algorithms.algorithm_base import AlgorithmBase
from maximum_matching.graphs.graph_base import BipartiteSet, GraphBase


class Oblivious(AlgorithmBase): 
    
    def run(self, graph: GraphBase) -> Tuple[int, Union[List, None]]:
        """
        Run Oblivious algorithm
        Based on "Greedy Online Bipartite Matching on Random Graphs"

        The oblivious algorithm performs a “one shot” trial for each unknown_node j, 
        where it attempts to match j to a random neighbor. 
        The algorithm is unaware of which known_nodes are already matched, 
        so an attempted match to an already matched known_nodes means that unknown_node j is dropped.

        :param graph: a graph instance from the BaseBipartiteGraph abstract
        :return: the final matching size with a list of matching size trend
        """

        print("Started running Oblivious")

        known_nodes = graph.b_get_independent_set(BipartiteSet.left)
        unknown_nodes = graph.b_get_independent_set(BipartiteSet.right)

        matched = {}
        visited_vertices = 0
        for known_node in known_nodes:
            visited_vertices += 1
            matched[known_node] = False

        count_matches = 0
        trends = []
        
        trends.append([visited_vertices, count_matches])

        for unknown_node in unknown_nodes:
            visited_vertices += 1
            neighbours = graph.list(unknown_node)

            if len(neighbours) > 0:
                random_id = random.randint(0, len(neighbours) - 1)
                random_neighbour = neighbours[random_id] - len(known_nodes)

                if matched.get(random_neighbour) is False:
                    matched[random_neighbour] = True
                    count_matches += 1

            trends.append([visited_vertices, count_matches])
        
        print("Finished running Oblivious")
        return [count_matches, trends]
