import random
from typing import Any

from maximum_matching.algorithms.algorithm_base import AlgorithmBase
from maximum_matching.graphs.graph_base import BipartiteSet, GraphBase


class Oblivious(AlgorithmBase): 
    
    def run(self, graph: GraphBase) -> Any:
        # print("Run Oblivious")
        known_nodes = graph.b_get_independent_set(BipartiteSet.left)
        unknown_nodes = graph.b_get_independent_set(BipartiteSet.right)

        matched = {}
        for known_node in known_nodes:
            print("known_node :", known_node)
            matched[known_node] = False

        count_matches = 0
        for unknown_node in unknown_nodes:
            # print("unknown_node :", unknown_node)
            neighbours = graph.list(unknown_node)

            if len(neighbours) > 0:
                random_id = random.randint(0, len(neighbours) - 1)
                random_neighbour = neighbours[random_id] - len(known_nodes)

                if matched.get(random_neighbour) is False:
                    matched[random_neighbour] = True
                    count_matches += 1
                elif matched.get(random_neighbour) is None:
                    print("unknown_node :", unknown_node)
                    print("Where is neighbour? :", random_neighbour)
        
        print("Matched: ", count_matches)
