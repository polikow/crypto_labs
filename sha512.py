from bitstring import Bits
from typing import List

# взял константы отсюда https://ru.bitcoinwiki.org/wiki/SHA-512
INITIAL = sum(Bits(uint=h, length=64) for h in
              [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
               0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]
              )

K = [Bits(uint=h, length=64) for h in
     [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538,
      0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe,
      0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
      0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
      0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab,
      0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
      0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed,
      0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
      0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
      0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
      0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373,
      0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
      0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c,
      0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
      0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
      0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]]


def parts(data: Bits, n: int) -> List[Bits]:
    """Разбиение данных на куски размера n"""
    assert data.len % n == 0
    assert n >= 1
    return [data[i * n: (i + 1) * n] for i in range(data.len // n)]


def padding(data: Bits) -> Bits:
    p = (-len(data) - 128) % 1024
    padding = Bits('0b1') + Bits(length=p - 1)

    data_length = Bits(uint=len(data), length=128)

    return data + padding + data_length


def extend_block(block: Bits) -> List[Bits]:
    """Блок 1024бит (16 слов) -> 5120бит (80 слов)"""
    words = parts(block, 64)  # изначальные 16 слов

    while len(words) != 80:
        i = len(words)
        w1 = words[i - 16]
        w2 = rot_shift(words[i - 15], 1, 8, 7)
        w3 = words[i - 7]
        w4 = rot_shift(words[i - 12], 19, 61, 6)
        words.append(w1 ^ w2 ^ w3 ^ w4)

    return words


def rot_shift(word: Bits, a: int, b: int, c: int) -> Bits:
    return (word >> a) ^ (word >> b) ^ (word << c)


def major_sum(a: Bits, b: Bits, c: Bits) -> Bits:
    return (a & b) ^ (b & c) ^ (c & a)


def conditional_sum(a: Bits, b: Bits, c: Bits) -> Bits:  # ошибка в книжке
    return (a & b) ^ (~a & c)


def cyclic_move(a: Bits) -> Bits:
    return (a >> 28) ^ (a >> 34) ^ (a >> 39)


def mod_sum(*args: Bits) -> Bits:
    """Сложение по модулю 2^64"""
    m = Bits('0b1') + Bits(length=64)
    res = sum(arg.uint for arg in args) % m.uint
    return Bits(uint=res, length=64)


def final_sum(digest: Bits, block: Bits) -> Bits:
    g1 = parts(digest, 64)
    g2 = parts(block, 64)
    return sum([mod_sum(w1, w2) for w1, w2 in zip(g1, g2)])


def sha512_round(digest: Bits, w: Bits, k: Bits) -> Bits:
    assert digest.len == 512
    a, b, c, d, e, f, g, h = parts(digest, 64)

    mix1 = mod_sum(major_sum(a, b, c), cyclic_move(a))
    mix2 = mod_sum(conditional_sum(e, f, g), cyclic_move(e), h, w, k)
    x = mod_sum(mix1, mix2)
    y = mod_sum(mix2, d)

    return sum((x, a, b, c, y, e, f, g))


def compress(digest: Bits, words: List[Bits]) -> Bits:
    """Функция сжатия. Применяется для каждого блока из 1024бит"""
    block = None
    for word, k in zip(words, K):
        if block is None:
            block = sha512_round(digest, word, k)
        else:
            block = sha512_round(block, word, k)

    return final_sum(digest, block)


def sha512(data: Bits) -> Bits:
    padded = padding(data)
    blocks = parts(padded, 1024)

    digest = None
    for block in blocks:
        if digest is None:
            words = extend_block(INITIAL)
            digest = compress(INITIAL, words)
        else:
            words = extend_block(block)
            digest = compress(digest, words)

    return digest


text = Bits('a'.encode('utf-8'))
digest = sha512(text)
