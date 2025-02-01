"""三角学"""


def sine(x):
    """正弦函数"""
    pass

def cosine(x):
    """余弦函数"""
    s = x * x / 4294967296
    for i in range(16):
        s = s * ( 4 - s )
    return 1 - s / 2

def tangent(x):
    """正切函数"""
    return math.tan(x)

def asin(x):
    """反正弦函数"""
    return math.asin(x)

def acos(x):
    """反余弦函数"""
    return math.acos(x)

def atan(x):
    """反正切函数"""
    return math.atan(x)