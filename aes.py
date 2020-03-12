# реализовать хотя бы 1 раунд аес
from bitstring import Bits
from typing import List
from aes_resources import *
from functools import reduce
from operator import xor


def state_matrix(bits128: Bits) -> List[List[Bits]]:
    """Конвертация битов в матрицу состояний"""
    s = [[Bits(length=0)] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            shift = i * 8 + j * 32
            s[i][j] = bits128[shift:shift + 8]

    return s


def sub_bytes(s: List[List[Bits]], inverse=False):
    """Обе подстановки"""
    table = INV_SUB if inverse else SUB

    for i in range(4):
        for j in range(4):
            bits8 = s[j][i]
            row = bits8[:4].uint
            col = bits8[4:].uint
            sub = table[row][col]
            s[j][i] = Bits(uint=sub, length=8)


def shift_rows(s: List[List[Bits]], inverse=False):
    for i in (1, 2, 3):
        row = s[i]
        if inverse:
            s[i] = row[-i:] + row[:-i]
        else:
            s[i] = row[i:] + row[:i]


def mix_columns(s: List[List[Bits]], inverse=False):
    """Оба преобразования колонок"""
    t = INV_MIX if inverse else MIX

    for i in range(4):
        for j in range(4):
            to_sum = []
            for c in range(4):
                a = s[c][j]
                b = t[j][c]
                to_sum.append(mult(a, b))
            s[i][j] = reduce(xor, to_sum)
            print()


def add_round_key(s: List[List[Bits]], key: Bits):
    """XOR ключа с матрицей состояний"""
    assert key.len == 128
    key = state_matrix(key)

    for i in range(4):
        for j in range(4):
            s[i][j] = s[i][j] ^ key[i][j]


def rem_zeros(bits: Bits) -> Bits:
    zeros = bits.bin.index('1')
    return bits[zeros:]


def mult(a: Bits, b: Bits) -> Bits:
    """Произведение полиномов в GF с образующим мн-ом (x8 + x4 + x3 + x + 1)"""
    to_sum = []

    for zeros, bit in enumerate(b[::-1]):
        if bit:
            to_sum.append(Bits(length=8 - zeros) + a + Bits(length=zeros))
    s = rem_zeros(reduce(xor, to_sum))

    while s.len >= POLYNOMIAL.len:
        zeros = s.len - POLYNOMIAL.len
        s = rem_zeros(s ^ (POLYNOMIAL + Bits(length=zeros)))

    zeros = 8 - s.len
    s = Bits(length=zeros) + s
    assert s.len == 8
    print(f'{a} * {b} = {s}')
    return s


def aes_round(s: List[List[Bits]], key: Bits, reverse=False):
    sub_bytes(s, reverse)  # работает
    shift_rows(s, reverse)  # работает
    mix_columns(s, reverse)
    add_round_key(s, key)


# text_s = 'big лепеха'
# key_s = 'small леха!?'

# text_s = 'Thats my Kung Fu'
key_s = 'Two One Nine Two'

text = Bits(hex='0x00041214120412000C00131108231919')
key = Bits(bytes(key_s, encoding='utf-8'))

s = state_matrix(text)
sub_bytes(s)  # работает
shift_rows(s)  # работает
mix_columns(s)
# aes_round(s, key)
# aes_round(s, key, reverse=True)
