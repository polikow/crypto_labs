# реализовать хотя бы 1 раунд аес
from bitstring import Bits
from typing import List
from aes_resources import *


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


text_s = 'big лепеха'
key_s = 'small леха!?'

text = Bits(bytes(text_s, encoding='utf-8'))
key = Bits(bytes(key_s, encoding='utf-8'))

s = state_matrix(text)
