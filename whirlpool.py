from functools import reduce
from operator import xor
from typing import List
from bitstring import Bits
from os import urandom

from aes import mult

S_BOX_RAW = """18 23 C6 E8 87 B8 01 4F 36 A6 D2 F5 79 6F 91 52
60 BC 9B 8E A3 0C 7B 35 1D E0 D7 C2 2E 4B FE 57
15 77 37 E5 9F F0 4A CA 58 C9 29 0A B1 A0 6B 85
BD 5D 10 F4 CB 3E 05 67 E4 27 41 8B A7 7D 95 C8
FB EE 7C 66 DD 17 47 9E CA 2D BF 07 AD 5A 83 33
63 02 AA 71 C8 19 49 C9 F2 E3 5B 88 9A 26 32 B0
E9 0F D5 80 BE CD 34 48 FF 7A 90 5F 20 68 1A AE
B4 54 93 22 64 F1 73 12 40 08 C3 EC DB A1 8D 3D
97 00 CF 2B 76 82 D6 1B B5 AF 6A 50 45 F3 30 EF
3F 55 A2 EA 65 BA 2F C0 DE 1C FD 4D 92 75 06 8A
B2 E6 0E 1F 62 D4 A8 96 F9 C5 25 59 84 72 39 4C
5E 78 38 8C C1 A5 E2 61 B3 21 9C 1E 43 C7 FC 04
51 99 6D 0D FA DF 7E 24 3B AB CE 11 8F 4E B7 EB
3C 81 94 F7 B9 13 2C D3 E7 6E C4 03 56 44 7F A9
2A BB C1 53 DC 0B 9D 6C 31 74 F6 46 AC 89 14 E1
16 3A 69 09 70 B6 C0 ED CC 42 98 A4 28 5C F8 86"""
S_BOX_NOT_SO_RAW = [Bits(hex=f'0x{el}') for el in S_BOX_RAW.replace('\n', ' ').split(' ')]
S_BOX = [S_BOX_NOT_SO_RAW[i * 16:(i + 1) * 16] for i in range(16)]

POLYNOMIAL = Bits('0b100011101')

MIX_RAW = """01 01 04 01 08 05 02 09
09 01 01 04 01 08 05 02
02 09 01 01 04 01 08 05
05 02 09 01 01 04 01 08
08 05 02 09 01 01 04 01
01 08 05 02 09 01 01 04
04 01 08 05 02 09 01 01
01 04 01 08 05 02 09 01
"""
MIX_NOT_SO_RAW = [Bits(hex=f'0x{el}') for el in MIX_RAW.replace('\n', ' ').split(' ')]
MIX = [MIX_NOT_SO_RAW[i * 8:(i + 1) * 8] for i in range(8)]


def parts(data: Bits, n: int) -> List[Bits]:
    """Разбиение данных на куски размера n"""
    return [data[i * n: (i + 1) * n] for i in range(data.len // n)]


def bits_to_state(bits512: Bits) -> List[List[Bits]]:
    """Конвертация битов в матрицу состояний"""
    parts8 = parts(bits512, 8)
    return [parts8[i * 8:(i + 1) * 8] for i in range(8)]


def sub_bytes(s: List[List[Bits]]):
    for i in range(8):
        for j in range(8):
            byte = s[j][i]
            row = byte[:4].uint
            col = byte[4:].uint
            s[j][i] = S_BOX[row][col]


def shift_cols(s: List[List[Bits]]):
    new_s = bits_to_state(Bits(length=512))

    for row in range(8):
        for col in range(8):
            index = (row + col) % 8
            new_s[row][col] = s[index][col]

    for i in range(8):
        s[i] = new_s[i]


def mix_rows(s: List[List[Bits]]):
    new_s = bits_to_state(Bits(length=512))

    for i in range(8):
        for j in range(8):
            new_s[i][j] = reduce(xor, [mult(s[i][c], MIX[c][j], POLYNOMIAL) for c in range(8)])

    for i in range(8):
        s[i] = new_s[i]


def add_round_key(s: List[List[Bits]], key: List[List[Bits]]):
    for i in range(8):
        for j in range(8):
            s[i][j] = s[i][j] ^ key[i][j]


def create_round_key(n: int) -> List[List[Bits]]:
    key = bits_to_state(Bits(length=512))
    key[0] = S_BOX_NOT_SO_RAW[n * 8: (n + 1) * 8]
    return key


text = Bits(urandom(64))
state = bits_to_state(text)

sub_bytes(state)

shift_cols(state)

mix_rows(state)

key1 = create_round_key(1)
add_round_key(state, key1)












