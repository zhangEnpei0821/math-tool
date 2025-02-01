"""常用函数"""


def factorial(integer: int) -> int:
    """阶乘"""

    if integer < 0:
        raise ValueError("Factorial is not defined for negative integers")
    
    if integer == 0:
        return 1
    
    number = 1
    for time in range(2, integer + 1):
        number *= time 
    
    return number

