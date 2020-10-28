from math import gcd as bltin_gcd, sqrt


def isPrime(num):
    if num > 1:
        for i in range(2, round(sqrt(num))):
            if (num % i) == 0:
                return False
                break
        else:
            return True

    else:
        return False


def coprime(a, b):
    return bltin_gcd(a, b) == 1


def isCongruent(number):
    # a - b = k * n
    # b = 3
    # k = 4
    # number - 3 = 4 * n
    if (number - 3) % 4 == 0:
        return True
    else:
        return False


