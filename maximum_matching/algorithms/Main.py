from Flags import Algorithms
from ..utility import Generator
from Vazirani import run_vazirani


def main():
    running_algorithms = [Algorithms.vazirani]
    gen = Generator()

    # Run the program
    test(gen, running_algorithms)


# Test the list of algorithms on the given generator
def test(generator, algorithms):
    randGraph = generator.generateBipartite()

    for i in algorithms:
        if i == Algorithms.vazirani:
            run_vazirani(randGraph)
