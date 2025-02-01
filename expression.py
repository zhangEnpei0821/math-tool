"""代数式"""


from mathematics.number import *


__all__ = ['Var', 'Monomial', 'Expression']


class Var:
    """数学变量"""

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return(self.string)
    
    def __repr__(self):
        return(self.string)


class Monomial:
    """单项式"""

    def __init__(self, coefficient, unknowns: dict):
        """初始化属性coefficient和unknowns"""
        if not isinstance(coefficient, (int, float, RationalNumber)):
            raise TypeError('coefficient must be a number')
        if not isinstance(unknowns, dict):
            raise TypeError('unknowns must be a dictionary')
        if not all(isinstance(k, Var) for k in unknowns.keys()):
            raise TypeError('unknowns keys must be vars')
        if not all(isinstance(v, (int, float, RationalNumber)) for v in unknowns.values()):
            raise TypeError('unknowns values must be numbers')
        self.coefficient = coefficient
        self.unknowns = unknowns
        self.reduce()
    
    def time(self) -> str:
        """返回单项式的次数"""
        time = 0
        for v in self.unknowns.values():
            time += v
        return time
    
    def __str__(self) -> str:
        """字符串表示"""
        s = ''
        if self.coefficient != 1 and self.coefficient != -1:
            s += str(self.coefficient)
        s += ''.join([str(k) + '^' + str(v) for k, v in self.unknown.items()])
        return s
    
    def reduce(self):
        items = self.unknowns.copy()
        for k, v in self.unknowns.items():
            if v == 0:
                del items[k]
        if self.unknowns.copy() == {}:
            return Monomial(0, {})
        return (self.coefficient, items)
    
    def value(self, var_value: dict):
        """带入求值"""
        new_coefficient = self.coefficient
        un = self.unknowns.copy()
        for k, v in self.unknowns.items():
            for i in var_value.keys():
                if k is i:
                    new_coefficient *= var_value[i] ** v
                    del un[k]
        if not un:
            return new_coefficient
        else:
            result = Monomial(new_coefficient, un)
            return result
    
    def __eq__(self, other) -> bool:
        """判断是否相等"""
        if isinstance(other, Monomial):
            return self.coefficient == other.coefficient and self.unknowns == other.unknowns
        return False
    
    def __hash__(self) -> int:
        """哈希值"""
        return hash((self.coefficient, tuple(self.unknowns.items())))
    
    def __pos__(self) -> 'Monomial':
        """取正"""
        return self
    
    def __neg__(self) -> 'Monomial':
        """取负"""
        return Monomial(-self.coefficient, self.unknowns)
    
    def __invert__(self) -> 'Monomial':
        """取倒数"""
        new_unknowns = {k: -v for k, v in self.unknowns.items()}
        new_coefficient = 1 / self.coefficient
        m = Monomial(new_coefficient, new_unknowns)
        return m
    
    def __abs__(self) -> 'Monomial':
        """取绝对值"""
        self.coefficient = abs(self.coefficient)
        return self
    
    def is_similar(self, other) -> bool:
        """判断是否为同类项"""
        if isinstance(other, Monomial):
            if self.unknowns == other.unknowns:
                return True
        return False
    
    def __add__(self, other) -> 'Monomial':
        """加法"""
        if isinstance(other, (int, float, RationalNumber)):
            return Expression([self], other)
        if isinstance(other, Monomial):
            if self.is_similar(other):
                self.coefficient += other.coefficient
                m = Monomial(self.coefficient, self.unknowns)
                return m
            else:
                return Expression([self, other], 0)
    
    def __radd__(self, other) -> 'Monomial':
        """右加法"""
        return self.__add__(other)
    
    def __sub__(self, other) -> 'Monomial':
        """减法"""
        return self.__add__(-other)
    
    def __rsub__(self, other) -> 'Monomial':
        """右减法"""
        return -self.__sub__(other)
    
    def __mul__(self, other) -> 'Monomial':
        """乘法"""
        if isinstance(other, (int, float, RationalNumber)):
            self.coefficient *= other
            m = Monomial(self.coefficient, self.unknowns)
            return m
        
        if isinstance(other, Monomial):
            new_unknowns = self.unknowns.copy()
            for k, v in other.unknowns.items():
                if k in new_unknowns:
                    new_unknowns[k] += v
                else:
                    new_unknowns[k] = v
            new_coefficient = self.coefficient * other.coefficient
            m = Monomial(new_coefficient, new_unknowns)
            return m
        
    def __truediv__(self, other) -> 'Monomial':
        """除法"""
        if isinstance(other, (int, float, RationalNumber)):
            self.coefficient /= other
            m = Monomial(self.coefficient, self.unknowns)
            return m
        
        if isinstance(other, Monomial):
            new_unknowns = self.unknowns.copy()
            for k, v in other.unknowns.items():
                if k in new_unknowns:
                    new_unknowns[k] -= v
                else:
                    new_unknowns[k] = -v
            new_coefficient = self.coefficient / other.coefficient
            m = Monomial(new_coefficient, new_unknowns)
            return m
    
    def __pow__(self, other) -> 'Monomial':
        """乘方"""
        if not isinstance(other, (int, float, RationalNumber)):
            raise TypeError('exponent must be a number')
        if other == 0:
            return Monomial(1, {})
        if other < 0:
            return 1 / self ** (-other)
        new_unknowns = {k: v * other for k, v in self.unknowns.items()}
        new_coefficient = self.coefficient ** other
        m = Monomial(new_coefficient, new_unknowns)
        return m
    
    def __repr__(self):
        """字符串表示"""
        s = ''
        if self.coefficient == -1:
            s += ' -'
            s += str(self.coefficient) + ' '
        for k, v in self.unknowns.items():
            s += str(k) + '^' + str(v)
        return s


class Expression:
    def __init__(self, monomials: list , constant=0):
        """初始化属性monomials和constant"""
        if not isinstance(monomials, list):
            raise TypeError('monomials must be a list')
        if not all(isinstance(m, Monomial) for m in monomials):
            raise TypeError('monomials must be a list of Monomial objects')
        if not isinstance(constant, (int, RationalNumber)):
            raise TypeError('constant must be a number')
        self.monomials = monomials
        self.constant = constant
    
    def __str__(self) -> str:
        """字符串表示"""
        s = ''
        if self.monomials:
            if self.monomials[0]:
                for m in self.monomials[0:]:
                    s += ' + ' + str(m)
        if self.constant != 0:
            s += ' + ' + str(self.constant)
        return s
    
    def value(self, var_value: dict):
        """带入求值"""
        value = Expression([], self.constant)
        value += sum(m.value(var_value) for m in self.monomials)
        return value
    
    def __eq__(self, other):
        return self.monomials == other.monomials and self.constant == other.constant
    
    def __add__(self, other) -> 'Expression':
        """加法"""
        new_monomials = self.monomials.copy()
        new_constant = self.constant

        if isinstance(other, (int, RationalNumber)):
            new_constant += other
        
        if isinstance(other, Monomial):
            found = False
            for m in new_monomials:
                if m.is_similar(other):
                    m.coefficient += other.coefficient
                    found = True
                    break
            if not found:
                new_monomials.append(other)
        
        if isinstance(other, Expression):
            for m in other.monomials:
                self += m
            self.constant += other.constant
            return self
        
        return Expression(new_monomials, new_constant)
    
    def __radd__(self, other) -> 'Expression':
        """右加法"""
        return self.__add__(other)
    
    def __sub__(self, other) -> 'Expression':
        """减法"""
        pass
    
    def __repr__(self) -> str:
        """字符串表示"""
        s = ''
        if self.monomials[0]:
            s += ' + '.join([str(m) for m in self.monomials])
            if self.constant != 0:
                s += ' + ' + str(self.constant)
        return s