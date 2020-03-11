# хотя бы 1 раунд дес и аес
from des_resources import EXTENSION, S_BOX, PERMUTE
from bitstring import Bits, BitArray


def p_block_extension(bits32: Bits) -> Bits:
    """P блок расширения"""
    bits48 = BitArray(length=48)

    for i, j in enumerate(EXTENSION):
        bits48[i] = bits32[j - 1]

    return Bits(bits48)


def s_blocks(bits48: Bits) -> Bits:
    """S блоки"""
    res = Bits(length=0)

    for i in range(8):
        bits6 = bits48[i:i + 6]
        row = Bits([bits6[0], bits6[5]]).uint
        column = bits6[1:5].uint
        number = S_BOX[i][row][column]
        bit4 = Bits(uint=number, length=4)
        res += bit4

    return res


def p_block_straight(bit32: Bits) -> Bits:
    """Прямая перестановка"""
    permuted32 = BitArray(length=32)

    for i in range(32):
        index = PERMUTE[i] - 1
        permuted32[i] = bit32[index]

    return Bits(permuted32)


def des_fun(bits: Bits, key: Bits) -> Bits:
    """Функция Фейстеля"""
    extended = p_block_extension(bits)
    xored = extended ^ key
    s_blocked = s_blocks(xored)
    res = p_block_straight(s_blocked)

    return res


def des_round(data: Bits, key: Bits) -> Bits:
    assert len(data) == 64
    assert len(key) == 48

    left = data[:32]
    right = data[32:]

    right_f = des_fun(right, key)
    new_right = left ^ right_f

    return right + new_right


def des_round_back(data: Bits, key: Bits) -> Bits:
    assert len(data) == 64
    assert len(key) == 48

    left = data[:32]
    right = data[32:]

    right_f_old = des_fun(left, key)
    old_left = right_f_old ^ right

    return old_left + left
