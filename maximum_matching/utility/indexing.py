def pdist_idx_ext(row, col, size) -> int:
    """
    Convert matrix row and col index to condensed matrix 1D index.
    Also counts for diagonal elements
    :param row: row of matrix (i)
    :param col: column of matrix (j)
    :param size: size of matrix
    :return: a condensed matrix index
    """
    if col < row:
        col, row = row, col
    return size * row - row * (row + 1) // 2 + col


def pdist_idx(row, col, size) -> int:
    """
    Convert matrix row and col index to condensed matrix 1D index.
    Does not include diagonal elements
    :param row: row of matrix (i)
    :param col: column of matrix (j)
    :param size: size of matrix
    :return: a condensed matrix index
    """
    assert row != col, "no diagonal elements in condensed matrix"
    if col < row:
        col, row = row, col
    return (size - 1) * row - row * (row + 1) // 2 + col
