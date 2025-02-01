"""数"""


from mathematics.number_theory import gcd, prime_factorization


__all__ = ['RationalNumber', 'RealNumber']


class RationalNumber:
    """
    有理数
    numerator:分子
    denominator:分母
    """

    def __init__(self, numerator, denominator):
        """初始化属性numerator和denominator"""
        if isinstance(numerator, float) or isinstance(denominator, float):
            raise ValueError("Unsupport dealing with floats")
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        if isinstance(numerator, int) and isinstance(denominator, int):
            self.numerator = numerator
            self.denominator = denominator
        if isinstance(numerator, RationalNumber) or isinstance(denominator, RationalNumber):
            self = numerator / denominator
    
    def __eq__(self, other) -> bool:
        """判断相等"""
        if isinstance(other, (float, int)):
            return self.numerator == other * self.denominator
        
        if isinstance(other, RationalNumber):
            return self.numerator * other.denominator == self.denominator * other.numerator
        
        raise TypeError("Invalid operand type for ==")
    
    def __ne__(self, other) -> bool:
        """判断不等"""
        return not self.__eq__(other)
    
    def __lt__(self, other) -> bool:
        """判断小于"""
        if isinstance(other, (int, float)):
            return self.denominator < other * self.numerator
        
        if isinstance(other, RationalNumber):
            return self.denominator * other.numerator < self.numerator * other.denominator
        
        raise TypeError("Invalid operand type for <")
    
    def __le__(self, other) -> bool:
        """判断小于等于"""
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other) -> bool:
        """判断大于"""
        return not self.__le__(other)
    
    def __ge__(self, other) -> bool:
        """判断大于等于"""
        return not self.__lt__(other)
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.numerator}/{self.denominator}"
    
    def __float__(self) -> float:
        """浮点数表示"""
        return float(self.numerator) / float(self.denominator)
    
    def __int__(self) -> int:
        """整数表示"""
        return int(float(self))
    
    def __abs__(self) -> "RationalNumber":
        """绝对值"""
        return RationalNumber(abs(self.numerator), abs(self.denominator))
    
    def __pos__(self) -> "RationalNumber":
        """取正"""
        return RationalNumber(self.numerator, self.denominator)
    
    def __neg__(self) -> "RationalNumber":
        """取负"""
        return RationalNumber(-self.numerator, self.denominator)
    
    def __round__(self, n=0) -> "RationalNumber":
        """四舍五入"""
        return RationalNumber(round(float(self), n), 1)
    
    def __floor__(self) -> "RationalNumber":
        """向下取整"""
        return RationalNumber(int(float(self)), 1)
    
    def __ceil__(self) -> "RationalNumber":
        """向上取整"""
        return RationalNumber(int(float(self) + 1), 1)
    
    def reduce(self) -> None:
        """约分"""
        factor = gcd(self.numerator, self.denominator)
        self.numerator = int(self.numerator / factor)
        self.denominator = int(self.denominator / factor)
        return self
    
    def __add__(self, other) -> "RationalNumber":
        """加法"""
        if isinstance(other, int):
            numerator = self.numerator + self.denominator * other
            r = RationalNumber(numerator, self.denominator)
        
        if isinstance(other, RationalNumber):
            numerator1 = self.numerator * other.denominator
            numerator2 = other.numerator * self.denominator
            numerator = numerator1 + numerator2
            denominator = self.denominator * other.denominator
            r = RationalNumber(numerator, denominator)
            r = r.reduce()
        
        return r
    
    def __radd__(self, other) -> "RationalNumber":
        """右加法"""
        return self.__add__(other)

    def __sub__(self, other) -> "RationalNumber":
        """减法"""
        return self.__add__(-other)
    
    def __rsub__(self, other) -> "RationalNumber":
        """右减法"""
        return -self.__sub__(other)
    
    def __mul__(self, other) -> "RationalNumber":
        """乘法"""
        if isinstance(other, int):
            numerator = self.numerator * other
            r = RationalNumber(numerator, self.denominator)
        
        if isinstance(other, RationalNumber):
            factor1 = gcd(self.denominator, other.numerator)
            factor2 = gcd(self.numerator, other.denominator)
            numerator = self.numerator * other.numerator / factor1 / factor2
            denominator = self.denominator * other.denominator / factor1 / factor2
            r = RationalNumber(int(numerator), int(denominator))
        
        return r

    def __rmul__(self, other) -> "RationalNumber":
        """右乘法"""
        return self.__mul__(other)

    def __truediv__(self, other) -> "RationalNumber":
        """除法"""
        if other == 0:
            raise ZeroDivisionError("division by zero")
        if isinstance(other, int):
            return self.__mul__(RationalNumber(1, other))
        if isinstance(other, RationalNumber):
            return self.__mul__(RationalNumber(other.denominator, other.numerator))


    def __rtruediv__(self, other) -> "RationalNumber":
        """右除法"""
        result =  self.__truediv__(other)
        return RationalNumber(result.denominator, result.numerator)
    
    def __pow__(self, other) -> "RationalNumber|RealNumber":
        """乘方"""
        if isinstance(other, int):
            if other == 0:
                return 1
            
            if other > 0:
                numerator = self.numerator ** other
                denominator = self.denominator ** other

            if other < 0:
                numerator = self.denominator ** -other
                denominator = self.numerator ** -other
            
            r = RationalNumber(numerator, denominator)
            return r
        
        if isinstance(other, RationalNumber):
            return RealNumber(self, other)
    
    def __repr__(self):
        return self.__str__()


class RealNumber:
    """
    实数
    coefficient:系数
    base:底数
    exponential:次数
    """

    def __init__(self, coefficient, base, exponential):
        """初始化属性coefficient,base和exponential"""
        self.coefficient = coefficient
        self.base = base
        self.exponential = exponential
    
    def __eq__(self, other):
        if isinstance(other, float):
            raise ValueError("Unsopport dealing with floats")
        r1 = self.reduce()
        if isinstance(other, RealNumber):
            r2 = self.reduce()
            if self._is_similar(other):
                if self.coefficient == other.coefficient:
                    return True
            return False
        if isinstance(other, int|RationalNumber):
            if r1.base == 1 or r1.exponential == 0:
                if r1.coefficient == other:
                    return True
                else:
                    return False

    def _is_similar(self, other) -> bool:
        """判断是否为同类项"""
        r1 = self.reduce()
        other = other.reduce()
        if isinstance(r1, RationalNumber):
            if isinstance(other, RationalNumber|int):
                return True
            else:
                return False
        if isinstance(r1, RealNumber):
            if isinstance(other, RationalNumber|int):
                return False
            if isinstance(other, RealNumber):
                if self.base == other.base and self.exponential == other.exponential:
                    return True
    
    def reduce(self) -> 'RationalNumber|RealNumber':
        """化简"""
        if isinstance(self.base, int):
            p_dict = prime_factorization(self.base)
            d = self.exponential.denominator
            for p, t in p_dict.items():
                if t >= d:
                    i = int((t / d))
                    self.base /= p ** (d ** i)
                    self.coefficient *= p ** i ** self.exponential.numerator
        return self
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.coefficient}*{self.base}^{self.exponential}"

    def __add__(self, other):
        pass
    
    def __repr__(self):
        return self.__str__()


class ContinuedFraction:
    """连分数"""

class ImaginaryNumber:
    """虚数"""

    def __init__(self, ceoefficient):
        """初始化属性ceoefficient"""
        self.ceoefficient = ceoefficient

class ComplexNumber:
    """复数"""

    def __init__(self, real, imaginary):
        """初始化属性real和imaginary"""
        self.real = real
        self.imaginary = imaginary