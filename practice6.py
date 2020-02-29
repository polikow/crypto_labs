from math import sqrt
from random import randint


def gcd(a: int, b: int) -> int:
    return abs(a) if b == 0 else gcd(b, a % b)


def is_prime(num):
    if num <= 1:
        return False

    res = True
    for x in range(2, int(sqrt(num) + 1)):
        if num % x == 0:
            res = False
            break
    return res


def primes():
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


def mersen_num(n):
    return 2 ** n - 1


def mersen(count):
    for n in range(1, count + 1):
        yield mersen_num(n)


def prime_mersen(count):
    for i, prime in enumerate(primes()):
        if i == count:
            break
        yield mersen_num(prime)


def ferma_num(n):
    return 2 ** 2 ** n + 1


def ferma(count):
    for n in range(0, count):
        yield ferma_num(n)


def ferma_test(n, k=100):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    for i in range(k):
        a = randint(1, n - 1)
        if gcd(n, a) != 1:
            return False
        if pow(a, n - 1, n) != 1:
            return False
    return True


def main():
    print(list(prime_mersen(5)))
    print(list(ferma(5)))  # первые 5 чисел простые

    print("Тест Ферма")
    for num in [23, 41, 15, 35, 561]:
        print(f'{num} - {"простое" if ferma_test(num) else "не простое"}')


if __name__ == '__main__':
    main()
