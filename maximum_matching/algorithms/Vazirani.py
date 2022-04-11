from random import shuffle
from Flags import BipartiteSet


class Vaz:
    def __init__(self, graph, generator):
        self.graph = graph
        self.generator = generator

    # Run Vazirani algorithm
    # Based on https://people.eecs.berkeley.edu/~vazirani/pubs/online.pdf
    # Given a bipartite graph G(U,V,E)
    # Assumption: Graphs are not necessarily complete [Contrary to the paper]
    # Let V = girls, U = boys, where U represents rows of an nxn matrix to vertices in U
    # Or in other words, boys and girls are two disjoint sets defined in a bipartite graph
    def run(self):
        # Assumption: Boys arrive first [left = boys, right = girls]
        boys = self.generator.getIndependantSet(self.graph, BipartiteSet.left)

        if boys is None or len(boys) == 0:
            print("Could not evaluate graph.")
            print("One of the disjoint sets are empty.")
            exit(0)

        # Priority is given to boys through their order in the array
        shuffle(boys)

        # Complete when there are no more vertices
        # Get the next vertex from the girls set

        print("running Vazirani ... ")

        nextV = self.generator.getNextVertexInSet(self.graph, BipartiteSet.right)
        while nextV is not None:
            nextV = self.generator.getNextVertexInSet(self.graph, BipartiteSet.right)

            # TODO incomplete

        return
