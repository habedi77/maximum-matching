# Check if the edge is a valid match for the maximum matching
def is_valid_match(max_matching: [], edge: []):
    v1 = edge[0]
    v2 = edge[1]

    # Check if any vertex from any edge in max_matching contains either of these two vertices
    for max_edge in max_matching:
        m1 = max_edge[0]
        m2 = max_edge[1]

        if m1 == v1 or m1 == v2 \
                or m2 == v1 or m2 == v2:
            return False

    return True


# Returns an edge from v1 to v2
def create_edge(v1, v2):
    return [v1, v2]
