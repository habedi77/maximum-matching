from typing import List

import maximum_matching.graphs as graphs
import maximum_matching.utility as util
import maximum_matching.algorithms as alg

import os, sys

sys.path.insert(0, os.path.abspath(".."))

generators = [
    util.GaussianGenerator(),
]

algorithms = [
    # alg.Vazirani(),
    alg.Oblivious()
]


# Test the list of algorithms on the given generator
def test(graph: graphs.GraphBase, algorithms: List[alg.AlgorithmBase]):
    for i in algorithms:
        i.run(graph)


# 'Main function'
if __name__ == "__main__":

    kwargs = {"mean": 10, "std": 1}

    # TODO
    for gen in generators:
        graph = gen.generate(size_left=100, size_right=100, seed=0,
                             graph_class=graphs.FullMatrixGraph, **kwargs)
        # Run the program
        test(graph, algorithms)
