import itertools
import math
import primes
from primes import is_prime_from_file, primes_from_file


def add(pol1, pol2):
    n1 = len(pol1)
    n2 = len(pol2)
    if n1 != n2:
        if n1 > n2:
            return tuple((a + b) % 2 for a, b in zip(pol1, (0,) * (n1 - n2) + pol2))
        else:
            return tuple((a + b) % 2 for a, b in zip((0,) * (n2 - n1) + pol1, pol2))

    return tuple((a + b) % 2 for a, b in zip(pol1, pol2))


def mult(pol1, pol2):
    pols = []
    for n, x in enumerate(reversed(pol2)):
        if x == 1:
            pols.append(pol1 + (0,) * n)
    res = sum_pols(*pols) if len(pols) != 1 else pols[0]
    return rem_zeros(res)[1]


def mult_pols(pols: list):
    if len(pols) < 1:
        raise Exception('беды с башкой')

    pol1 = pols.pop()
    while len(pols) >= 1:
        pol2 = pols.pop()
        pol1 = mult(pol1, pol2)

    return pol1


def power(*pols):
    res = 0
    for pol in pols:
        res += len(pol) - 1
    return res


def sum_pols(*pols):
    if len(pols) == 1:
        if len(pols[0]) != 0:
            return pols[0][0]
        else:
            return (0,)
    if len(pols) == 0:
        return (0,)
    else:
        return add(add(pols[0], pols[1]), sum_pols(pols[2:]))


def rem_zeros(pol):
    try:
        i = pol.index(1)
        return i, pol[i:]
    except ValueError:
        return 0, (0,)


def div(pol1, pol2):
    p1, p2 = power(pol1), power(pol2)

    if p2 == 0 and pol2[0] == 0:
        raise Exception('деление на 0')

    if p1 < p2:
        return (0,), pol1

    quotient = ()
    while p1 >= p2 and pol1 != (0,):
        removed, new_pol = rem_zeros(add(pol1, pol2 + (0,) * (p1 - p2)))
        new_p = power(new_pol)

        if new_pol == (0,):
            quotient += (1,) + (0,) * (p1 - p2)
            pol1, p1 = new_pol, new_p
            break

        if p1 != p2:
            zeros = removed - 1
        else:
            zeros = 0
        if new_p + 1 < zeros:
            if removed <= p2 + 1:
                zeros -= 1
        if zeros > (p1 - p2):
            zeros = (p1 - p2)
        quotient += (1,) + (0,) * zeros
        pol1, p1 = new_pol, new_p

    return quotient, pol1


def generate_pols(pow, min=0):
    pols = [rem_zeros(pol)[1] for pol in itertools.product((0, 1), repeat=pow)]
    if min == 0:
        return pols
    else:
        return filter(lambda pol: 1 if power(pol) >= min else 0, pols)


def mult_table_op(pol1, pol2, pol):
    _, remainder = div(mult(pol1, pol2), pol)
    return remainder


def mult_table(k, pol):
    if k < 2 or k > 4:
        raise Exception('беды с башкой')

    pols = generate_pols(k)
    return pols, [[mult_table_op(pol1, pol2, pol) for i, pol2 in enumerate(pols)]
                  for j, pol1 in enumerate(pols)]


def generate_power(k):
    return (1,) + (0,) * k


def euler(a):
    res = 0
    for num in range(1, a + 1):
        if math.gcd(a, num) == 1:
            res += 1
    return res


def is_prime(pol):
    """Неприводимый ли многочлен"""
    p = power(pol)
    if p == 0:
        return False, None
    if p == 1:
        return True, None

    max_p = int(math.sqrt(p) + 1)

    for pol2 in generate_pols(max_p, min=1):
        quotient, rem = div(pol, pol2)
        if rem == (0,):
            return False, (quotient, pol2)
    return True, None


def primes(power):
    """Генератор неприводимых многочленов"""
    for pol in generate_pols(power + 1, min=1):
        if is_prime(pol)[0]:
            yield pol


def primes_dict(power):
    res = {i: [] for i in range(1, power + 1, 1)}
    for pol in primes(power + 1):
        pols = res.get(power(pol))
        pols.append(pol)
    return res


def mutually_prime(a, b):
    """Взаимно простые числа"""
    if a == 0 or b == 0:
        return False
    return math.gcd(a, b) == 1


def is_primitive(pol):
    if not is_prime(pol)[0]:
        return False

    n = power(pol)
    start = n + 1
    stop = 2 ** n - 2

    for q in range(start, stop + 1, 1):
        tmp = (1,) + (0,) * (q - 1) + (1,)
        _, rem = div(tmp, pol)
        if rem == (0,):
            return False

    return True


def gcd(pol1, pol2):
    """НОД для полиномов по АЕ"""
    p1, p2 = power(pol1), power(pol2)
    if p1 < p2:
        return gcd(pol2, pol1)
    else:
        quotient, remainder = div(pol1, pol2)
        if remainder == (0,):
            return pol2
        else:
            return gcd(pol2, remainder)


def gf_elements(k, pol):
    """Элементы поля 2^k для образующего многочлена pol"""
    n = 2 ** k
    pols = []
    for i in range(n):
        _, remainder = div((1,) + (0,) * i, pol)
        pols.append(remainder)
    return pols


def cycle_powers(k, pol_power):
    """Цикломатический класс для GF(2^k)"""
    if pol_power < 1:
        raise Exception('беды с башкой')

    max = 2 ** k
    for i in range(k):
        power = pol_power * 2 ** i
        yield power if power < max else power % (max - 1)


def cycle_sorted(k, pol_power):
    return sorted(cycle_powers(k, pol_power))


def test(power):
    for p in range(1, power + 1, 1):
        primes = primes_from_file(p)
        print(f'{primes} = {mult_pols(primes)}')


def mod(pol1, pol2):
    _, remainder = div(pol1, pol2)
    return remainder


if __name__ == '__main__':
    div((1, 1, 1, 1, 1, 1), (1, 1, 1))
    div((1, 1, 1, 1), (1, 1, 1))
    div((1, 1, 0, 1), (1, 0))
    div((1, 1, 0, 1), (1, 1))

    assert is_primitive((1, 1, 1))
    assert is_primitive((1, 1, 0, 1))
    assert is_primitive((1, 0, 0, 1, 1))
    assert is_primitive((1, 0, 0, 1, 1))
    assert is_primitive((1, 1, 0, 1, 1, 1))
    assert is_primitive((1, 1, 1, 1, 0, 1))
