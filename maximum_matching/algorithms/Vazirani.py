from random import shuffle
from Flags import BipartiteSet


# Returns the 'other' vertex associated with the edge
# Let an edge be A -> B, for vertices A and B
# Of {A,B} this returns: vertex - {A,B}
def op_vertex_of_edge(vertex, edge):
    # TODO
    # Need to merge branch with proper Generator to complete
    # For edge implementation

    return -1


# Check if the edge is a valid match for the maximum matching
def is_valid_match(self, max_matching, edge):
    # TODO
    # Need to merge branch with proper Generator to complete
    # For edge implementation

    return


class Vaz:
    def __init__(self, graph, generator, rand_order):
        self.graph = graph
        self.generator = generator
        self.rand_order = rand_order

    # Run Vazirani algorithm
    # Based on https://people.eecs.berkeley.edu/~vazirani/pubs/online.pdf
    # Given a bipartite graph G(U,V,E)
    # Assumption: Graphs are not necessarily complete [Contrary to the paper]
    # Let V = girls, U = boys, where U represents rows of an nxn matrix to vertices in U
    # Or in other words, boys and girls are two disjoint sets defined in a bipartite graph
    # Return the maximum_matching. Or well, the 'estimated' best matching.
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

        girls = self.generator.getIndependantSet(BipartiteSet.right)

        # Randomize the order of girl vertices
        if self.rand_order:
            shuffle(girls)

        max_matching = []

        for vertex in girls:
            # As each girl arrives, match her to the eligible boy of the highest rank
            edges_of_vertex = self.generator.getEdgesOfVertex(vertex)

            # Check neighbours. Match with the eligible boy (if any) of the highest rank
            valid_matches = []  # Pick highest rank out of the possible valid matches
            for edge in edges_of_vertex:
                if is_valid_match(max_matching, edge):
                    valid_matches.append([edge, boys.index(op_vertex_of_edge(vertex, edge))])

            highest_rank = []
            for i in valid_matches:
                if i[1] < highest_rank:
                    highest_rank = i

            # Use the edge to the highest ranked eligible boy
            if len(highest_rank > 0):
                max_matching.append(highest_rank[0])

            valid_matches.clear()

        return max_matching
