from gf import add, mult, div, mult_table
from polynomial_repr import polynomial as pol_str, polynomial_01 as pol_01, \
    mult_str, superscript


def div_str(a, b):
    q, r = div(a, b)
    a, b, q, r = pol_str(a), pol_str(b), pol_str(q), pol_str(r)
    return "({})/({}) = ({})({}) + ({})".format(a, b, q, b, r)


def mult_str2(a, b):
    return '({})({}) = {}'.format(pol_str(a), pol_str(b), pol_str(mult(a, b)))


def table_str(k, pol):
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

    return '\n'.join(
        ['Таблица умножения в GF(2{}) c образующим многочленом {} ({})'.format(superscript(k),pol_01(pol),pol_str(pol))]
        + new_buf)


def main():
    print(mult_str2((1, 1, 1, 0), (1, 0, 1)))
    print(div_str((1, 1, 1, 0), (1, 0, 1)))
    print(table_str(3, (1, 1, 0, 1)))
    print(table_str(3, (1, 0, 1, 1)))
    print(table_str(4, (1, 1, 0, 0, 1)))


if __name__ == '__main__':
    main()
