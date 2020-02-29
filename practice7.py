from functools import reduce

from gf_repr import str_to_polynomial as old_kek


def lin_congruential(n, x0, a, c, m):
    """Линейный конгруэнтный метод. Xn+1 = (aXn + c) mod m"""
    if n == 0:
        return x0
    else:
        x_prev = lin_congruential(n - 1, x0, a, c, m)
        return (a * x_prev + c) % m


def task_1(n=10):
    parameters = [
        (4, 6, 7, 10),
        (4, 4, 5, 9),
        (7, 7, 7, 10),
        (5, 5, 3, 8),
        (5, 3, 3, 17),
        (2, 7, 4, 9),
    ]

    for x0, a, c, m in parameters:
        print(f"Xn+1 = ({a}Xn + {c}) mod {m}, X0 = {x0}")
        for i in range(n):
            print(lin_congruential(i, x0, a, c, m), end=', ')
        print('\n')


def task_3():
    parameters = [
        ('x4 + x + 1', (1, 0, 1, 0)),
        ('x5 + x3 + x', (1, 0, 1, 0, 1)),
        ('x4 + x3 + 1', (1, 0, 1, 0)),
        ('x5 + x2 + 1', (1, 0, 1, 0, 0)),
        ('x4 + x3 + 1', (0, 1, 0, 1)),
        ('x5 + x3 + x2 + x + 1', (0, 1, 1, 0, 1)),
    ]

    for f, state in parameters:
        lin_recur_shift(f, state)


def str_to_polynomial(pol):
    return old_kek(pol)[:0:-1]


def lin_recur_shift(fun, state):
    fun = str_to_polynomial(fun)
    f = ()
    prev_states = []
    prev_f = []
    prev_g = []
    assert len(fun) == len(state)

    found = None
    while found is None:
        prev_states.append(state)
        prev_f.append(f)
        g = reduce(lambda a, b: (a + b) % 2, (a * b for a, b in zip(fun, state)))
        prev_g.append(g)

        f = f + state[:1]
        state = state[1:] + (g,)

        for prev in prev_states:
            if state == prev:
                found = prev

    prev_states.append(state)
    prev_f.append(f)
    prev_g.append(reduce(lambda a, b: (a + b) % 2, (a * b for a, b in zip(fun, state))))

    i = prev_states.index(found)
    j = len(prev_states) - 1

    prev_f = [''.join((str(i) for i in prev_f_)) for prev_f_ in prev_f]
    prev_states = [''.join((str(i) for i in prev_state)) for prev_state in prev_states]

    f_width = max([len(f) for f in prev_f])
    state_width = len(state)

    print(f'T = {j - i}')
    print('{:^{f_width}}|{:>{state_width}}|{}'
          .format('f(x)', ''.join((str(i) for i in fun)), 'g', f_width=f_width, state_width=state_width))
    print('-' * (state_width + f_width + 3))
    for n, (f, state, g) in enumerate(zip(prev_f, prev_states, prev_g)):
        pointer = '<-' if n == i or n == j else ''
        print('{:>{f_width}}|{:>{state_width}}|{} {}'
              .format(f, state, g, pointer, f_width=f_width, state_width=state_width))
    print()
    return j - i


task_3()
