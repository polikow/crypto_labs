from gf import add, mult, div
from polynomial_repr import polynomial, polynomial_01


def div_print(a, b):
    q, r = div(a, b)
    a, b, q, r = polynomial(a), polynomial(b), polynomial(q), polynomial(r)
    print("({})/({}) = ({})({}) + ({})".format(a, b, q, b, r))


def test():
    a = (1, 1, 1, 0)
    b = (1, 0, 1)
    text = '({})({}) = {}'.format(polynomial(a), polynomial(b), polynomial(mult(a, b)))
    print(text)

    polynomials = [
        (1, 1, 0),
        (1,),
        (0,),
        (1, 1),
        (1, 1, 0, 1, 1),
    ]

    for pol in polynomials:
        print(polynomial(pol), end=' или ')
        print(polynomial_01(pol))


if __name__ == '__main__':
    test()
