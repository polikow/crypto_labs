superscript_map = {
    "0": "⁰", "1": "¹", "2": "²",
    "3": "³", "4": "⁴", "5": "⁵",
    "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}

superscript_translation = str.maketrans(
    ''.join(superscript_map.keys()),
    ''.join(superscript_map.values()))


def superscript(num, one=False):
    res = str(num).translate(superscript_translation)
    if one:
        return res
    else:
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
                buf.append('+')

    return ''.join(buf)


def polynomial_01(pol: tuple):
    return ''.join([str(x) for x in pol])


def digits(num):
    for i in map(int, str(num)):
        yield i


def only_01(pol):
    for x in pol:
        if not (x == 0 or x == 1):
            raise Exception('беды с башкой')


def num_to_polynomial(num):
    if not isinstance(num, int):
        raise Exception('неправильный')

    pol = tuple(digits(num))
    only_01(pol)
    if len(pol) == 0:
        pol = (num,)
    return pol


def str_to_polynomial(s):
    if not isinstance(s, str):
        raise Exception('неправильный тип')

    elems = s.split('+')
    powers = []
    for el in elems:
        try:
            powers.append(int(el.replace('x', '')) if el.__contains__('x') else (0 if int(el) == 1 else None))
        except ValueError:  # вероятнее всего el = 'x'
            powers.append(1)
    size = max(powers) + 1
    res = [0] * size

    for p in powers:
        res[size - p - 1] = 1

    return tuple(res)


def convert_pols(*pols):
    res = []
    for pol in pols:
        if not isinstance(pol, tuple):
            if isinstance(pol, int):
                res.append(num_to_polynomial(pol))
            elif isinstance(pol, str):
                res.append(str_to_polynomial(pol))
            else:
                raise Exception('неправильный тип')
        else:
            res.append(pol)

    return res


if __name__ == '__main__':
    print(convert_pols(101, 1, 0, 10, 'x2+x1+1', 'x3 + x1 + 1'))
