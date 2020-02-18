import itertools


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
    return rem_zeros(res)


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
        return pol[pol.index(1):]
    except ValueError:
        return (0,)


def calc_quotient(new_p, p1, p2):
    if new_p >= p2:
        return (1,) + (0,) * (p1 - new_p - 1)
    return (1,)


def div(pol1, pol2):
    p1, p2 = power(pol1), power(pol2)

    if p1 < p2:
        return (0,), pol1

    quotient = ()
    while p1 >= p2:
        new_pol = rem_zeros(add(pol1, pol2 + (0,) * (p1 - p2)))
        new_p = power(new_pol)
        quotient += calc_quotient(new_p, p1, p2)
        pol1 = new_pol
        p1 = new_p

    return quotient, pol1


def generate_pols(k):
    return [rem_zeros(pol) for pol in itertools.product((0, 1), repeat=k)]


def mult_table_op(pol1, pol2, pol):
    _, remainder = div(mult(pol1, pol2), pol)
    return remainder


def mult_table(k, pol):
    if k < 2 or k > 4:
        raise Exception('беды с башкой')

    pols = generate_pols(k)
    return pols, [[mult_table_op(pol1, pol2, pol) for i, pol2 in enumerate(pols)]
                     for j, pol1 in enumerate(pols)]


if __name__ == '__main__':
    # print(mult_table_op((1,), (1, 1, 0), (1, 1, 0, 1)))
    for row in mult_table(3, (1, 1, 0, 1)):
        print(row)
