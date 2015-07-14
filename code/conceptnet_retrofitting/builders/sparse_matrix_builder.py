from scipy import sparse

class SparseMatrixBuilder:
    """
    SparseMatrixBuilder is a utility class that helps build a matrix of
    unknown shape.
    """

    def __init__(self):
        self.rowIndex = []
        self.colIndex = []
        self.values = []

    def __setitem__(self, key, val):
        row, col = key
        self.rowIndex.append(row)
        self.colIndex.append(col)
        self.values.append(val)

    def tocsr(self, shape, dtype=float):
        return sparse.coo_matrix((self.values, (self.rowIndex, self.colIndex)),
                                shape=shape, dtype=dtype).tocsr()
