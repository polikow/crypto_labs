import gf
from gf_repr import polynomial as pol_str, polynomial_01 as pol_01, superscript, convert_pols
from primes import primes as file_primes


def add(a, b, pretty=True):
    a, b = convert_pols(a, b)
    res = gf.add(a, b)

    convert = pol_str if pretty else pol_01
    a, b, res = convert(a), convert(b), convert(res)
    print(f'{a} + {b} = {res}')


def divide(a, b, pretty=True):
    a, b = convert_pols(a, b)
    q, r = gf.div(a, b)

    convert = pol_str if pretty else pol_01
    a, b, q, r = convert(a), convert(b), convert(q), convert(r)
    r = f'+ {r}' if r != '0' else ''
    print(f"{a} / {b} = {q} {r}")


def multiply(a, b, pretty=True):
    a, b = convert_pols(a, b)
    res = gf.mult(a, b)

    convert = pol_str if pretty else pol_01
    a, b, res = convert(a), convert(b), convert(res)
    print(f'{a} * {b} = {res}')


def gcd(a, b, pretty=True):
    a, b = convert_pols(a, b)
    res = gf.gcd(a, b)

    convert = pol_str if pretty else pol_01
    a, b, res = convert(a), convert(b), convert(res)
    print(f'gcd({a}, {b}) = {res}')


def mod(a, b, pretty=True):
    a, b = convert_pols(a, b)
    res = gf.mod(a, b)

    convert = pol_str if pretty else pol_01
    a, b, res = convert(a), convert(b), convert(res)
    print(f'{a} mod {b} = {res}')


def eval_primes(power, pretty=True):
    convert = pol_str if pretty else pol_01

    for prime in gf.primes(power):
        if pretty:
            print(f'{gf.power(prime)}) {convert(prime)}')


def primes(power, pretty=True):
    convert = pol_str if pretty else pol_01

    for i, prime in enumerate(file_primes[power]):
        print(f'{i + 1}) {convert(prime)}')


def is_primitive_smart(pol):
    pol, = convert_pols(pol)
    k = gf.power(pol)

    primitive = True
    for i, element in enumerate(gf.gf_elements(k, pol)):
        print(f'x{superscript(i)} = {pol_str(element)}')
        if i == 0 or i == 2**k - 1:
            continue
        else:
            if element == (1,):
                primitive = False
                break

    print('Примитивный' if primitive else 'Не примитивный', '\n')


def cyclomatic_classes(pol1, k, pol0):
    if pol1 == 'all':
        pol0, = convert_pols(pol0)
        classes = gf.all_cyclomatic_classes(k)
    else:
        pol1, pol0 = convert_pols(pol1, pol0)
        pol_power = gf.power(pol1)
        classes = [list(gf.cyclomatic_elems(k, pol_power))]

    """вычисление элементов каждого класса"""
    cyclomatic_classes = []
    for class_ in classes:
        cyclomatic_class = []
        for el_power in class_:
            tmp = (1,) + (0,) * el_power
            if el_power < k:
                cyclomatic_class.append(tmp)
            else:
                remainder = gf.mod(tmp, pol0)
                cyclomatic_class.append(remainder)
        cyclomatic_classes.append(cyclomatic_class)

    factors = gf.factorize(k)

    """нахождение минимальных многочленов"""
    found = False
    min_pols = {}
    for factor in filter(lambda factor: gf.power(factor) == k, factors):
        for cyclomatic_class in cyclomatic_classes:
            for pol in filter(lambda pol: gf.power(pol) > 1, cyclomatic_class):
                if gf.mod(gf.sub(factor, pol), pol0) == (0,):
                    found = True
                break
            if found:
                break
        if found:
            min_pols[factor] = cyclomatic_class
            found = False

    title = f'Цикломатический класс для многочлена {pol_str(pol1)}\n' if pol1 != 'all' else 'Цикломатические классы\n'
    print(title, f'над полем GF(2{superscript(k)}) c образующим многочленом {pol_str(pol0)}')

    factors_str = ''.join([f'({pol_str(pol)})' for pol in factors])
    factorized = pol_str(convert_pols(f'x{2 ** k - 1} + 1')[0])
    print(f'{factorized} = {factors_str}')

    for class_, cyclomatic_class in zip(classes, cyclomatic_classes):
        print('{{ {} }}'.format(', '.join([f'x{superscript(el)}' for el in class_])), end=' = ')
        print('{{ {} }}'.format(', '.join([pol_str(p) for p in cyclomatic_class])), end=' ')
        for factor, pols in min_pols.items():
            if pols == cyclomatic_class:
                print(f'для F{factors.index(factor) + 1} ({pol_str(factor)})')
                break
    print()


def multiplication_table(k, pol):
    pol, = convert_pols(pol)
    headers, table = gf.mult_table(k, pol)
    headers = [pol_str(header) for header in headers]
    width = len(max(headers, key=len))
    table = [[pol_01(pol) for pol in row] for row in table]

    buf = [''.join(['{:^{width}}'.format(header, width=width) for header in headers]),
           '_' * width * len(headers)]
    for row in table:
        buf.append(''.join(['{:^{width}}'.format(pol, width=width) for pol in row]))

    new_buf = []
    for header, row in zip(['', '', ] + headers, buf):
        if header == '':
            new_buf.append('{:^{width}}'.format(header, width=width) + row)
        else:
            new_buf.append('{:^{width}}|'.format(header, width=width) + row)
    new_buf.append('\n')

    print('\n', '\n'.join(
        ['Таблица умножения в GF(2{}) c образующим многочленом {} ({})'.format(superscript(k), pol_01(pol),
                                                                               pol_str(pol))]
        + new_buf))


def primitive_elements(k, pol):
    pol, = convert_pols(pol)
    buf = []
    for i, elem in enumerate(gf.gf_elements(k, pol)):
        buf.append("x{} = {} {}"
                   .format(superscript(i, one=True), pol_str(elem),
                           ' примитивный' if gf.is_mutually_prime(2 ** k - 1, i) else ''))

    print("\nпримитивные элементы ({} эл-ов) GF(2{}) для образующего многочлена {} ({})"
          .format(gf.euler(2 ** k - 1), superscript(k), pol_01(pol), pol_str(pol)))
    print('\n'.join(buf), '\n')


def is_primitive(pol):
    pol, = convert_pols(pol)
    print('{} - примитивен'.format(pol_str(pol)) if gf.is_primitive(pol) else '{} - НЕ примитивен'.format(pol_str(pol)))
