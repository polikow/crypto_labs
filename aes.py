# реализовать хотя бы 1 раунд аес
from typing import List
from aes_resources import *
from functools import reduce
from operator import xor


def bits_to_state(bits128: Bits) -> List[List[Bits]]:
    """Конвертация битов в матрицу состояний"""
    s = [[Bits(length=0)] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            shift = i * 8 + j * 32
            s[i][j] = bits128[shift:shift + 8]

    return s


def state_to_bits(s: List[List[Bits]]) -> Bits:
    to_sum = []
    for i in range(4):
        for j in range(4):
            to_sum.append(s[j][i])
    return sum(to_sum)


def sub_bytes(s: List[List[Bits]], reverse=False):
    """Обе подстановки"""
    table = INV_SUB if reverse else SUB

    for i in range(4):
        for j in range(4):
            bits8 = s[j][i]
            row = bits8[:4].uint
            col = bits8[4:].uint
            sub = table[row][col]
            s[j][i] = Bits(uint=sub, length=8)


def shift_rows(s: List[List[Bits]], reverse=False):
    for i in (1, 2, 3):
        row = s[i]
        if reverse:
            s[i] = row[-i:] + row[:-i]
        else:
            s[i] = row[i:] + row[:i]


def mix_columns(s: List[List[Bits]], reverse=False):
    """Оба преобразования колонок"""
    table = INV_MIX if reverse else MIX
    new_s = bits_to_state(Bits(length=128))

    for i in range(4):
        for j in range(4):
            new_s[i][j] = reduce(xor, [mult(s[c][j], table[i][c]) for c in range(4)])

    for i in range(4):
        s[i] = new_s[i]


def add_round_key(s: List[List[Bits]], key: Bits):
    """XOR ключа с матрицей состояний"""
    assert key.len == 128
    key = bits_to_state(key)

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
    return s


def aes_round(s: List[List[Bits]], key: Bits):
    sub_bytes(s)
    shift_rows(s)
    mix_columns(s)
    add_round_key(s, key)


def aes_round_reverse(s: List[List[Bits]], key: Bits):
    add_round_key(s, key)
    mix_columns(s, reverse=True)
    shift_rows(s, reverse=True)
    sub_bytes(s, reverse=True)
