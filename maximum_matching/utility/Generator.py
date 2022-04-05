# Template
# Generator class
# Used to generate a random bipartite graph
class Gen:
    def __init__(self):
        return

    # Returns a random bipartite graph of the given degree
    # TODO
    def generateBipartiteDeg(self, degree):
        return

    # Returns a random bipartite graph
    # TODO
    def generateBipartite(self):
        return

    # Returns length number of vertices as an array from the 'left' (one) disjoint set
    # Set can be left or right (From Flags.BipartiteSet)
    # This function is less important, might not end up needing it
    # FIXME Note: May want to move this into the class for the Bipartite graphs [If you find it makes more sense]
    def getIndependantSetOfLen(self, graph, length, set):
        return

    # Returns all vertices as an array from one disjoint set
    # Set can be left or right (From Flags.BipartiteSet)
    # FIXME Note: May want to move this into the class for the Bipartite graphs [If you find it makes more sense]
    def getIndependantSet(self, graph, set):
        return

    # Returns the next vertex in the bipartite graph from the given set
    # The online algorithms will call this until all vertices have been evaluated
    # Set can be left or right (From Flags.BipartiteSet)
    # FIXME Note: May want to move this into the class for the Bipartite graphs [If you find it makes more sense]
    # When there are no vertices left, return None
    def getNextVertexInSet(self, graph, set):
        return

    # Returns the next vertex in the bipartite graph
    # The online algorithms will call this until all vertices have been evaluated
    # FIXME Note: May want to move this into the class for the Bipartite graphs [If you find it makes more sense]
    # When there are no vertices left, return None
    def getNextVertex(self, graph):
        return

    # Return the edges of the given vertex
    # FIXME Note: May want to move this into the class for the Bipartite graphs [If you find it makes more sense]
    # Note: All vertices should have atleast one edge.
    def getEdgesOfVertex(self, vertex):
        return
