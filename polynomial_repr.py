from gf import sum_pols, power

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


def polynomial_01(pol: tuple):
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
            buf_adds.append('{:>{length}}'.format(polynomial_01(pol1) + ' ' * n, length=length))
    res = sum_pols(*pols) if len(pols) != 1 else pols[0]

    buf = ['{:>{length}}'.format(polynomial_01(pol1), length=length),
           '{:>{length}}'.format(polynomial_01(pol2), length=length)]
    if len(buf_adds) > 1:
        buf.append('-' * length)
        buf += buf_adds
    buf.append('-' * length)
    buf.append('{:>{length}}'.format(polynomial_01(res), length=length))
    return '\n'.join(buf)
