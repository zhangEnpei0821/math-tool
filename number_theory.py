"""数论"""


from pathlib import Path
import json


# this list only includes prime numbers that are below 100
p_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def gcd(integer1, integer2) -> int:
    """两个整数的最大公因数"""
    if not isinstance(integer1, int) or not isinstance(integer2, int):
        raise ValueError("Input numbers must be integers")
    
    if integer1 < 0:
        integer1 *= -1
    
    if integer2 < 0:
        integer2 *= -1
    
    if integer1 == 0 or integer2 == 0:
        raise ValueError("gcd is not defined for 0")
    
    while integer2 != 0:
        integer1, integer2 = integer2 , integer1 % integer2
    
    return integer1


def lcm(integer1, integer2) -> int:
    """两个整数的最小公倍数"""
    if not isinstance(integer1, int) or not isinstance(integer2, int):
        raise ValueError("Input numbers must be integers")
    
    if integer1 < 0:
        integer1 *= -1
    
    if integer2 < 0:
        integer2 *= -1
    
    if integer1 == 0 or integer2 == 0:
        raise ValueError("lcm is not defined for 0")
    
    return integer1 * integer2 // gcd(integer1, integer2)


def gcf(*integers) -> int:
    """一组整数的最大公因数"""

    if len(integers) < 2:
        raise ValueError("At least two integer is required")

    result = integers[0]
    for integer in integers[1:]:
        result = gcd(result, integer)

    return result


def lcf(*integers) -> int:
    """一组整数的最小公倍数"""

    if len(integers) == 0:
        raise ValueError("At least one integer is required")

    if len(integers) == 1:
        return integers[0]

    result = integers[0]
    for integer in integers[1:]:
        result = lcm(result, integer)

    return result


def find_prime_number():
    """寻找质数"""

    path1 = Path('prime_numbers.json')
    contents1 = path1.read_text()
    prime_numbers = json.loads(contents1)

    path2 = Path('last_number.json')
    contents2 = path2.read_text()
    last_number = json.loads(contents2)

    for i in range(100):
        a = 0
        while True:
            if mt.gcd(last_number, prime_numbers[a]) == 1:
                a += 1
                if a == len(prime_numbers):
                    prime_numbers.append(last_number)
                    last_number += 1
                    break
            else:
                last_number += 1
                break

    contents3 = json.dumps(prime_numbers)
    path1.write_text(contents3)

    contents4 = json.dumps(last_number)
    path2.write_text(contents4)


def prime_factorization(integer) -> dict:
    """质因数分解"""

    if not isinstance(integer, int):
        raise ValueError("Input number must be integer")
    if integer <= 1:
        raise ValueError("Input number must be greater than 1")
    
    facted_p_numbers = {}

    for i in range(24):
        p = p_numbers[i]
        if p > integer:
            break
        while True:
            if integer % p == 0:
                if p in facted_p_numbers:
                    facted_p_numbers[p] += 1
                else:
                    facted_p_numbers[p] = 1
                integer /= p
            else:
                break
    
    return facted_p_numbers


def divisors(integer) -> list:
    """所有因子"""

    if not isinstance(integer, int):
        raise ValueError("Input number must be integer")
    if integer <= 0:
        raise ValueError("Input number must be greater than 0")
    
    divs = []
    for i in range(1, integer + 1):
        if integer % i == 0:
            divs.append(i)
    
    return divs


def iteration(start, function, time):
    """迭代"""
    list = [start]
    for i in range(time):
        start = function(start)
        list.append(start)
    return list
