from gf import add, mult, div
from polynomial_repr import polynomial as pol_str, polynomial_01 as pol_01, \
    mult_str


def div_str(a, b):
    q, r = div(a, b)
    a, b, q, r = pol_str(a), pol_str(b), pol_str(q), pol_str(r)
    print("({})/({}) = ({})({}) + ({})".format(a, b, q, b, r))


def test():
    a = (1, 1, 1, 0)
    b = (1, 0, 1)
    text = '({})({}) = {}'.format(pol_str(a), pol_str(b), pol_str(mult(a, b)))
    print(text)

    polynomials = [
        (1, 1, 0),
        (1,),
        (0,),
        (1, 1),
        (1, 1, 0, 1, 1),
    ]

    for pol in polynomials:
        print(pol_str(pol), end=' или ')
        print(pol_01(pol))


if __name__ == '__main__':
    test()
