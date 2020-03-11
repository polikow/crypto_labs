from des import *

text_s = 'леха'
key_s = 'lepeha'

text = Bits(bytes(text_s, encoding='utf-8'))
key = Bits(bytes(key_s, encoding='utf-8'))

encrypted = des_round(text, key)
decrypted = des_round_back(encrypted, key)

print(f'открытый текст = {text}')
print(f'ключ           = {key}')
print(f'шифротекст     = {encrypted}')
print(f'дешифрованный  = {decrypted}')

print(f'открытый текст utf8 = {text_s}')
print(f'дешифрованный utf8  = {decrypted.bytes.decode("utf-8")}')