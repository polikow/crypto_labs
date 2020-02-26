import gf
from gf_repr import polynomial as pol_str, polynomial_01 as pol_01, mult_str, superscript, convert_pols


def divide(a, b, pretty=True):
    a, b = convert_pols(a, b)
    q, r = gf.div(a, b)
    if pretty:
        a, b, q, r = pol_str(a), pol_str(b), pol_str(q), pol_str(r)
        print("({})/({}) = ({}) {}".format(a, b, q, f'+ {r}' if r != '0' else ''))
    else:
        a, b, q, r = pol_01(a), pol_01(b), pol_01(q), pol_01(r)
        print("{} / {} = {} {}".format(a, b, q, f'+ {r}' if r != '0' else ''))


def multiply(a, b, pretty=True):
    a, b = convert_pols(a, b)
    if pretty:
        print('({})({}) = {}'.format(pol_str(a), pol_str(b), pol_str(gf.mult(a, b))))
    else:
        print('{} * {} = {}'.format(pol_01(a), pol_01(b), pol_01(gf.mult(a, b))))


def gcd(a, b, pretty=True):
    a, b = convert_pols(a, b)
    if pretty:
        print('gcd({}, {}) = {}'.format(pol_str(a), pol_str(b), pol_str(gf.gcd(a, b))))
    else:
        print('gcd({}, {}) = {}'.format(pol_01(a), pol_01(b), pol_01(gf.gcd(a, b))))


def mod(a, b, pretty=True):
    a, b = convert_pols(a, b)
    res = gf.mod(a, b)

    convert = pol_str if pretty else pol_01
    a, b, res = convert(a), convert(b), convert(res)
    print(f'{a} mod {b} = {res}')


def primes(power, pretty=True):
    for prime in gf.primes(power):
        if pretty:
            print('{}) {}'.format(gf.power(prime), pol_str(prime)))
        else:
            print('{}) {}'.format(gf.power(prime), pol_01(prime)))


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
                           ' примитивный' if gf.mutually_prime(2 ** k - 1, i) else ''))

    print("\nпримитивные элементы ({} эл-ов) GF(2{}) для образующего многочлена {} ({})"
          .format(gf.euler(2 ** k - 1), superscript(k), pol_01(pol), pol_str(pol)))
    print('\n'.join(buf), '\n')


def is_primitive(pol):
    pol, = convert_pols(pol)
    print('{} - примитивен'.format(pol_str(pol)) if gf.is_primitive(pol) else '{} - НЕ примитивен'.format(pol_str(pol)))
