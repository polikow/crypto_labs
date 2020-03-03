import itertools

from gf_repr import str_to_polynomial as old_kek
from functools import reduce


def str_to_polynomial(pol):
    return old_kek(pol)[:0:-1]


def psp_general(n, x0, a, c, m):
    if n == 0:
        return x0
    else:
        x_prev = psp_general(n - 1, x0, a, c, m)
        return (a * x_prev + c) % m


def shift(f: list, state: list, g: int):
    f = f + state[:1]
    state = state[1:] + (g,)
    return f, state


def lin_recur_shift(pol, state):
    pol = str_to_polynomial(pol)
    f = ()
    prev_states = []
    prev_f = []
    prev_g = []
    assert len(pol) == len(state)

    found_el = None
    found = False
    while not found:
        prev_states.append(state)
        prev_f.append(f)
        prev_g.append(g)

        g = (state[0] + state[1]) % 2
        f, state = shift(f, state, g)
        for prev in prev_states:
            if state == prev:
                found = True
                found_el = prev

    i = prev_states.index(found_el)
    j = len(prev_states)

    prev_f = [''.join(prev_f_) for prev_f_ in prev_f]
    prev_states = [''.join(prev_state) for prev_state in prev_states]

    f_width = max([len(f) for f in prev_f])
    state_width = len(state)

    for f, state, g in zip(prev_f, prev_states, prev_g):
        print('{:>{f_width}}|{:>{state_width}}|{}'.format(f, state, g, f_width=f_width, state_width=state_width))

    print('kek', j - i)
    return j - i


def zad1_2():
    # задание 1
    parameters = [
        (4, 6, 7, 10),
        (4, 4, 5, 9),
        (7, 7, 7, 10),
        (5, 5, 3, 8),
        (5, 3, 3, 17),
        (2, 7, 4, 9),
        # (2, 13, 11, 24),
    ]
    n = 5
    for x0, a, c, m in parameters:
        for i in range(n):
            print(psp_general(i, x0, a, c, m), end=' ')
        print()


def m_sequence(seq: str):
    for k in range(4, 1, -1):
        try:
            t = 2 ** k - 1
            if seq.index(seq[:k], t) == t:
                ones = reduce(lambda a, b: int(a) + int(b), list(seq[:t]))
                if not (ones == 2 ** (k - 1)):
                    continue

                for sub in [''.join(s) for s in list(itertools.product(('0', '1'), repeat=k))][1:]:
                    seq.index(sub)
                return seq[:t]

        except ValueError:
            continue

    return 'нет'


def zad4():
    sequences = [
        '1110000101011001110000101011',
        '1010110101011010101101010110',
        '0000011101011100000011101011',
        '0100100001111100100100001111',
        '0011010111100010011010111100',

        '0000011101011100000011101011',
        '0100100001111100100100001111',
        '1110000101011001110000101011',
        '0011101001110100111010011101',
        '0011010111100010011010111100',

        '0000011101011100000011101011',
        '0100100001111100100100001111',
        '0011010111100010011010111100',
        '1010110101011010101101010110',
        '1010110101011010101101010110',

        '1110000101011001110000101011',
        '1010110101011010101101010110',
        '0000011101011100000011101011',
        '0100100001111100100100001111',
        '0011010111100010011010111100',
    ]
    for i, seq in enumerate(sequences):
        print(f'{i + 1} {m_sequence(seq)}')


def main():
    zad4()


if __name__ == '__main__':
    main()
