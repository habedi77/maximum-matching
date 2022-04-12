import maximum_matching.graphs as graphs
import maximum_matching.utility.generator as generator
from maximum_matching.algorithms.Vazirani import Vaz

# Test the list of algorithms on the given generator
def test(generator, algorithms):
    for i in algorithms:
        i.run()


# 'Main function'
if __name__ == "__main__":
    gen = Gen()
    randGraph = gen.generateBipartite()

    running_algorithms = [Vaz(randGraph, gen)]

    # Run the program
    test(gen, running_algorithms)
