import maximum_matching.graphs as graphs
import maximum_matching.utility.generator as generator
from maximum_matching.algorithms.vazirani import Vazirani

import os, sys
sys.path.insert(0, os.path.abspath(".."))

generators = [
    generator.GaussianBipartiteGenerator(),
]

algorithms = [
    Vazirani(),
]


# Test the list of algorithms on the given generator
def test(graph, algorithms):
    for i in algorithms:
        i.run(graph)


# 'Main function'
if __name__ == "__main__":

    kwargs = {"mean": 10, "std": 1}

    # TODO
    for gen in generators:
        graph = gen.generate(size_left=100, size_right=100, seed=0,
                             graph_class=graphs.full_matrix.FullMatrixGraph, **kwargs)
        # Run the program
        test(graph, algorithms)
