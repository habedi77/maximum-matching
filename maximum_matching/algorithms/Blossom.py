from .algorithm_base import AlgorithmBase


class Bloss(AlgorithmBase):
    def __init__(self):
        pass

    # TODO
    # Find an augmented path from vertex v
    def augmented_path(self, v):

        neighbours = self.generator.getEdgesOfVertex(v)

        for i in neighbours:
            # TODO find augmenting path

            break

        return []

    # Remove elements from a list
    def remove_from_list(self, to_remove, list):

        for i in to_remove:
            list.remove(i)

        return list

    # Modified from https://en.wikipedia.org/wiki/Blossom_algorithm
    def blossom(self, graph, matching, exposed_vertices):

        # Find all augmenting paths
        while len(exposed_vertices > 0):
            p = self.augmented_path(exposed_vertices)

            # Vertices along path are no longer exposed
            if len(p) != 0:
                self.remove_from_list(exposed_vertices, p)
            else:
                # TODO
                # Add matched vertices to matching list

                break

            return

        return

    # Run the Blossom Algorithm
    # Based on what we learned in class
    # Does NOT include blossoms, since there are no odd cycles [Just augmentation]
    # Return the maximum_matching. Or well, the 'estimated' best matching.
    # This is NOT an online algorithm.
    # This is to determine how close an online algorithm is to being optimal
    def run(self, graph):
        return self.blossom(self, graph, [], graph)
