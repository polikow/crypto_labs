superscript_map = {
    "0": "⁰", "1": "¹", "2": "²",
    "3": "³", "4": "⁴", "5": "⁵",
    "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}

superscript_translation = str.maketrans(
    ''.join(superscript_map.keys()),
    ''.join(superscript_map.values()))


def superscript(num):
    res = str(num).translate(superscript_translation)
    return res if res != "¹" else ''


def plus(power, pol):
    n = len(pol)
    for x in pol[n - power:]:
        if x == 1:
            return True
    return False


def power(*pols):
    res = 0
    for pol in pols:
        res += len(pol) - 1
    return res


def enumeratedown(iterable):
    n = len(iterable) - 1
    for i, x in enumerate(iterable):
        yield n - i, x


def polynomial(pol: tuple):
    if len(pol) == 1 and pol[0] == 0:
        return '0'

    buf = []
    for power, x in enumeratedown(pol):
        if x == 1:
            if power > 0:
                buf.append('x')
                buf.append(superscript(power))
            else:
                buf.append(str(x))
            if plus(power, pol):
                buf.append(' + ')

    return ''.join(buf)


def polynomial_short(pol: tuple):
    buf = []
    for x in pol:
        buf.append(str(x))
    return ''.join(buf)


def mult_string(pol1, pol2):
    length = power(pol1, pol2) + 1
    buf_adds = []
    pols = []
    for n, x in enumerate(reversed(pol2)):
        if x == 1:
            pols.append(pol1 + (0,) * n)
            buf_adds.append('{:>{length}}'.format(polynomial_short(pol1) + ' ' * n, length=length))
    res = sum_pols(*pols) if len(pols) != 1 else pols[0]

    buf = ['{:>{length}}'.format(polynomial_short(pol1), length=length),
           '{:>{length}}'.format(polynomial_short(pol2), length=length)]
    if len(buf_adds) > 1:
        buf.append('-' * length)
        buf += buf_adds
    buf.append('-' * length)
    buf.append('{:>{length}}'.format(polynomial_short(res), length=length))
    return '\n'.join(buf)


def mult(pol1, pol2):
    pols = []
    for n, x in enumerate(reversed(pol2)):
        if x == 1:
            pols.append(pol1 + (0,) * n)
    return sum_pols(*pols) if len(pols) != 1 else pols[0]


def add(pol1, pol2):
    n1 = len(pol1)
    n2 = len(pol2)
    if n1 != n2:
        if n1 > n2:
            return tuple((a + b) % 2 for a, b in zip(pol1, (0,) * (n1 - n2) + pol2))
        else:
            return tuple((a + b) % 2 for a, b in zip((0,) * (n2 - n1) + pol1, pol2))

    return tuple((a + b) % 2 for a, b in zip(pol1, pol2))


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
        raise Exception('беды с башкой')

    quotient = ()
    while p1 >= p2:
        new_pol = rem_zeros(add(pol1, pol2 + (0,) * (p1 - p2)))
        new_p = power(new_pol)
        quotient += calc_quotient(new_p, p1, p2)
        pol1 = new_pol
        p1 = new_p

    return quotient, pol1


a = (1, 1, 1, 0, 1, 1)
b = (1, 1)
q, r = div(a, b)
a, b, q, b, r = polynomial(a), polynomial(b), polynomial(q), polynomial(b), polynomial(r)
print("({})/({}) = ({})({}) + ({})".format(a, b, q, b, r))
#
# a = (1, 1, 1, 0)
# b = (1, 0, 1)
# text = '({})({}) = {}'.format(polynomial(a), polynomial(b), polynomial(mult(a, b)))
# print(text)

polynomials = [
    (1, 1, 0),
    (1,),
    (0,),
    (1, 1),
    (1, 1, 0, 1, 1),
]

for pol in polynomials:
    print(polynomial(pol), end=' или ')
    print(polynomial_short(pol))
