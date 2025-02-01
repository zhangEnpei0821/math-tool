"""微积分"""

def limit(f, x, side=""):
    """极限"""
    

def derivative(f, x):
    """导数"""
    return limit(lambda h: (f(x+h) - f(x)) / h, 0)