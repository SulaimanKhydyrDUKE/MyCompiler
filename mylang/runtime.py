class Matrix:
    def __init__(self, data):
        self.data = data # List of lists of integers
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __repr__(self):
        return "[" + ", ".join(str(row) for row in self.data) + "]"

    def transpose(self):
        new_data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(new_data)

    def is_invertible(self):
        if self.rows != self.cols:
            return False
        # Simple determinant check for small matrices or rank check
        return self.determinant() != 0

    def has_null(self):
        # A matrix has a non-trivial null space if it's not full column rank
        # For simplicity, we'll check if rank < cols
        return self.rank() < self.cols

    def reduce(self):
        # Gaussian elimination to Row Echelon Form
        res = [row[:] for row in self.data]
        if not res: return Matrix(res)
        
        pivot_row = 0
        for j in range(self.cols):
            if pivot_row >= self.rows: break
            
            # Find pivot
            best_row = pivot_row
            for i in range(pivot_row + 1, self.rows):
                if abs(res[i][j]) > abs(res[best_row][j]):
                    best_row = i
            
            if res[best_row][j] == 0:
                continue
                
            res[pivot_row], res[best_row] = res[best_row], res[pivot_row]
            
            # Eliminate other rows
            for i in range(self.rows):
                if i != pivot_row:
                    factor = res[i][j] / res[pivot_row][j]
                    for k in range(j, self.cols):
                        res[i][k] -= factor * res[pivot_row][k]
            
            # Normalize pivot row
            divisor = res[pivot_row][j]
            for k in range(j, self.cols):
                res[pivot_row][k] /= divisor
            
            pivot_row += 1
            
        # Convert back to integers if possible, or keep as floats for precision
        # MyLang.txt says Matrix is 2D array of Integers, but Reduce might result in floats.
        # We'll round for now to keep it "Integer-ish" or just return floats.
        return Matrix([[round(x, 2) for x in row] for row in res])

    def determinant(self):
        if self.rows != self.cols: return 0
        if self.rows == 1: return self.data[0][0]
        if self.rows == 2:
            return self.data[0][0]*self.data[1][1] - self.data[0][1]*self.data[1][0]
        
        # Simple recursive determinant (not efficient for large matrices)
        det = 0
        for j in range(self.cols):
            minor = [row[:j] + row[j+1:] for row in self.data[1:]]
            det += ((-1)**j) * self.data[0][j] * Matrix(minor).determinant()
        return det

    def rank(self):
        # Rank is number of non-zero rows in Reduced Echelon Form
        reduced = self.reduce()
        rank = 0
        for row in reduced.data:
            if any(abs(x) > 1e-9 for x in row):
                rank += 1
        return rank

