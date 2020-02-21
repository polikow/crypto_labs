from gf import *
from polynomial_repr import polynomial as pol_str, polynomial_01 as pol_01, mult_str, superscript, convert_pols


def divide(a, b, pretty=True):
    a, b = convert_pols(a, b)
    q, r = div(a, b)
    if pretty:
        a, b, q, r = pol_str(a), pol_str(b), pol_str(q), pol_str(r)
        print("({})/({}) = ({}) {}".format(a, b, q, f'+ {r}' if r != '0' else ''))
    else:
        a, b, q, r = pol_01(a), pol_01(b), pol_01(q), pol_01(r)
        print("{} / {} = {} {}".format(a, b, q, f'+ {r}' if r != '0' else ''))


def multiply(a, b, pretty=True):
    a, b = convert_pols(a, b)
    if pretty:
        print('({})({}) = {}'.format(pol_str(a), pol_str(b), pol_str(mult(a, b))))
    else:
        print('{} * {} = {}'.format(pol_01(a), pol_01(b), pol_01(mult(a, b))))


def gcd(a, b, pretty=True):
    a, b = convert_pols(a, b)
    if pretty:
        print('gcd({}, {}) = {}'.format(pol_str(a), pol_str(b), pol_str(gcd_gf(a, b))))
    else:
        print('gcd({}, {}) = {}'.format(pol_01(a), pol_01(b), pol_01(gcd_gf(a, b))))


def all_primes(pow, pretty=True):
    for prime in primes(pow + 1):
        if pretty:
            print('{}) {}'.format(power(prime), pol_str(prime)))
        else:
            print('{}) {}'.format(power(prime), pol_01(prime)))


def table_str(k, pol):
    pol, = convert_pols(pol)
    headers, table = mult_table(k, pol)
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
    for i, elem in enumerate(gf_elements(k, pol)):
        buf.append("x{} = {} {}"
                   .format(superscript(i, one=True), pol_str(elem),
                           ' примитивный' if mutually_prime(2 ** k - 1, i) else ''))

    print("\nпримитивные элементы ({} эл-ов) GF(2{}) для образующего многочлена {} ({})"
          .format(euler(2 ** k - 1), superscript(k), pol_01(pol), pol_str(pol)))
    print('\n'.join(buf), '\n')


def main():
    divide(1011, 11)
    multiply(1011, 11)
    print('\n')
    divide(101, 11)
    multiply(101, 11)
    print('\n')
    divide(1101, 101)
    multiply(1101, 101)
    print('\n')
    divide(10101, 111)
    multiply(10101, 111)
    print('\n')
    divide(10111, 11)
    multiply(10111, 11)
    print('\n')
    divide(101101, 111)
    multiply(101101, 111)

    print('\n')
    gcd(100001, 1111)
    gcd(110001, 11011)
    gcd(10001, 101101)
    gcd(111010, 101110)

    pols = [11, 111,
            101, 1010,
            1011, 1100,
            1101, 1110,
            1111, 10001,
            10011, 10100,
            10101, 1111,
            11001, 11101,
            11111, 101011,
            101101, 111001,
            111111,
            110101, 101001,
            100101, 100011]
    pols = convert_pols(*pols)

    print('\n')
    for i, pol in enumerate(pols):
        is_pr, a = is_prime(pol)
        is_prim = is_primitive(pol)
        text = ''
        if not is_pr and isinstance(a, tuple):
            text = '= ({})({})'.format(pol_str(a[0]), pol_str(a[1]))

        print('{}) {} {} {}'.format(i + 1, pol_str(pol),
                                    'неприводимый' if is_pr else text,
                                    'и примитивный' if is_prim else ''))

    table_str(3, 1101)
    table_str(3, 1011)

    primitive_elements(3, 1101)
    primitive_elements(3, 1011)
    primitive_elements(4, 11001)
    primitive_elements(4, 10011)


if __name__ == '__main__':
    main()
