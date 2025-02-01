"""线性代数"""


import math


class Vector:
    """向量"""

    def __init__(self, coordinates: list):
        self.coordinates = coordinates

    def __str__(self) -> str:
        """字符串表示"""
        return f'Vector: {self.coordinates}'

    def __repr__(self) -> str:
        return f'Vector: {self.coordinates}'
    
    def dimension(self) -> int:
        """维数"""
        return len(self.coordinates)

    def __eq__(self, other):
        """判断相等"""
        return self.coordinates == other.coordinates

    def __add__(self, other):
        """相加"""
        return Vector([x + y for x, y in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other):
        """相减"""
        return Vector([x - y for x, y in zip(self.coordinates, other.coordinates)])

    def __mul__(self, other: int | float):
        """数乘"""
        return Vector([x*other for x in self.coordinates])

    def __rmul__(self, other):
        """右乘法"""
        return self.__mul__(other)

    def norm(self):
        """模"""
        return (sum([x**2 for x in self.coordinates])) ** 0.5

    def unit(self):
        """单位向量"""
        mag = self.norm()
        return Vector([x/mag for x in self.coordinates])

    def dot(self, other):
        """点积"""
        return sum([x*y for x, y in zip(self.coordinates, other.coordinates)])

    def angle(self, other):
        """
        夹角
        在0和pi之间
        """
        mag1 = self.norm()
        mag2 = other.norm()
        dot_product = self.dot(other)
        return math.acos(dot_product / mag1 / mag2)

    def cross(self, other):
        """叉积"""
        x1, y1, z1 = self.coordinates
        x2, y2, z2 = other.coordinates
        return Vector([y1*z2 - y2*z1, z1*x2 - z2*x1, x1*y2 - x2*y1])


class Matrix:
    """矩阵"""

    def __init__(self, matrix: list):
        self.matrix = matrix

    def __str__(self) -> str:
        """字符串表示"""
        return f'Matrix: {self.matrix}'

    def __repr__(self) -> str:
        return f'Matrix: {self.matrix}'

    def __eq__(self, other):
        """判断相等"""
        return self.matrix == other.matrix

    def __add__(self, other):
        """相加"""
        return Matrix([[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(self.matrix, other.matrix)])

    def __sub__(self, other):
        """相减"""
        return Matrix([[x - y for x, y in zip(row1, row2)] for row1, row2 in zip(self.matrix, other.matrix)])

    def __mul__(self, other):
        """矩阵乘法"""
        if isinstance(other, Matrix):
            if self.num_columns() != other.num_rows():
                raise ValueError('Number of columns in first matrix must be equal to number of rows in second matrix.')
            return Matrix([[sum([self.matrix[i][k] * other.matrix[k][j] for k in range(self.num_columns())]) for j in range(other.num_columns())] for i in range(self.num_rows())])
        elif isinstance(other, Vector):
            if self.num_columns() != other.dimension():
                raise ValueError('Number of columns in matrix must be equal to dimension of vector.')
            return Vector([sum([self.matrix[i][k] * other.coordinates[k] for k in range(self.num_columns())]) for i in range(self.num_rows())])
        else:
            return Matrix([[x*other for x in row] for row in self.matrix])

    def __rmul__(self, other):
        """右乘法"""
        return self.__mul__(other)

    def num_rows(self) -> int:
        """行数"""
        return len(self.matrix)

    def num_columns(self) -> int:
        """列数"""
        return len(self.matrix[0])

    def transpose(self):
        """转置"""
        return Matrix([[self.matrix[j][i] for j in range(self.num_rows())] for i in range(self.num_columns())])

    def determinant(self):
        """行列式"""
        if self.num_rows() != self.num_columns():
            raise ValueError('Matrix must be square.')
        if self.num_rows() == 1:
            return self.matrix[0][0]
        elif self.num_rows() == 2:
            return self.matrix[0][0]*self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0]
        else:
            det = 0
            for j in range(self.num_columns()):
                minor = self.submatrix(0, j)
                det += ((-1) ** j) * self.matrix[0][j] * minor.determinant()
            return det

    def submatrix(self, i: int, j: int):
        """子矩阵"""
        return Matrix([[self.matrix[x][y] for y in range(self.num_columns()) if y != j] for x in range(1, self.num_rows())])

    def inverse(self):
        """逆矩阵"""
        if self.num_rows() != self.num_columns():
            raise ValueError('Matrix must be square.')
        det = self.determinant()
        if det == 0:
            raise ValueError('Matrix is not invertible.')
        cofactors = []
        for i in range(self.num_rows()):
            cofactor_row = []
            for j in range(self.num_columns()):
                minor = self.submatrix(i, j)
                cofactor_row.append(((-1) ** (i+j)) * minor.determinant())
            cofactors.append(cofactor_row)
        cofactors = Matrix(cofactors).transpose()
        return (1/det) * cofactors