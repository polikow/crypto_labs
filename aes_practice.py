from aes import *

from bitstring import Bits

text_s = 'big лепеха'
key_s = 'small леха!?'

text = Bits(bytes(text_s, encoding='utf-8'))
key = Bits(bytes(key_s, encoding='utf-8'))

s = bits_to_state(text)
aes_round(s, key)
encrypted = state_to_bits(s)
aes_round_reverse(s, key)
decrypted = state_to_bits(s)
res = state_to_bits(s)

print(f'открытый текст = {text}  ({text.bytes.decode("utf-8")} в utf-8)')
print(f'ключ           = {key}  ({key.bytes.decode("utf-8")} в utf-8)')
print(f'шифротекст     = {encrypted}  ({encrypted.bytes.decode("utf-8", errors="replace")} в utf-8)')
print(f'дешифрованный  = {decrypted}  ({decrypted.bytes.decode("utf-8")} в utf-8)')
