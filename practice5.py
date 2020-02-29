from gf_commands import *


def main():
    cyclomatic_classes('x', 5, 'x5 + x2 + 1')
    cyclomatic_classes('x3', 5, 'x5 + x2 + 1')
    cyclomatic_classes('x5', 5, 'x5 + x2 + 1')
    cyclomatic_classes('x7', 5, 'x5 + x2 + 1')
    cyclomatic_classes('all', 5, 'x5 + x2 + 1')
    cyclomatic_classes('all', 5, 'x5 + x3 + x2 + x + 1')

    # они все примитивные
    is_primitive_smart(100101)
    is_primitive_smart(110111)
    is_primitive_smart(1011011)
    is_primitive_smart(1100001)

    # для демонстрации
    is_primitive_smart(1111)


if __name__ == '__main__':
    main()
