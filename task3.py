from gf_repr import *


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
            111111, 111101,
            110101, 101001,
            100101, 100011]
    pols = convert_pols(*pols)

    print('\n')
    for i, pol in enumerate(pols):
        is_pr, a = gf.is_prime(pol)
        is_prim = gf.is_primitive(pol)
        text = ''
        if not is_pr and isinstance(a, tuple):
            text = '= ({})({})'.format(pol_str(a[0]), pol_str(a[1]))

        print('{}) {} {} {}'.format(i + 1, pol_str(pol),
                                    'неприводимый' if is_pr else text,
                                    'и примитивный' if is_prim else ''))


if __name__ == '__main__':
    main()
