"""运算"""


def dichotomy(function, left, right, epsilon=1e-6) -> float:
    """二分法求根"""

    if not callable(function):
        raise ValueError("Input function must be callable")
    if left >= right:
        raise ValueError("Left endpoint must be less than right endpoint")
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")
    
    left_value = function(left)
    right_value = function(right)
    if left_value * right_value > 0:
        raise ValueError("Function must have opposite signs at endpoints")
    
    while abs(right - left) > epsilon:
        mid = (left + right) / 2
        mid_value = function(mid)
        if mid_value * left_value < 0:
            right = mid
            right_value = mid_value
        else:
            left = mid
            left_value = mid_value
    
    return (left + right) / 2


def newton_method(function, derivative, initial_guess, epsilon=1e-6) -> float:
    """牛顿法求根"""

    if not callable(function):
        raise ValueError("Input function must be callable")
    if not callable(derivative):
        raise ValueError("Input derivative must be callable")
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")
    
    x = initial_guess
    while True:
        fx = function(x)
        dfx = derivative(x)
        if abs(fx) < epsilon:
            return x
        x -= fx / dfx
