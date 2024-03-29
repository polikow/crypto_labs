from des import *

text_s = 'леха'
key_s = 'lepeha'

text = Bits(bytes(text_s, encoding='utf-8'))
key = Bits(bytes(key_s, encoding='utf-8'))

encrypted = des_round(text, key)
decrypted = des_round_reverse(encrypted, key)

print(f'открытый текст = {text}  ({text.bytes.decode("utf-8")} в utf-8)')
print(f'ключ           = {key}  ({key.bytes.decode("utf-8")} в utf-8)')
print(f'шифротекст     = {encrypted}  ({encrypted.bytes.decode("utf-8", errors="replace")} в utf-8)')
print(f'дешифрованный  = {decrypted}  ({decrypted.bytes.decode("utf-8")} в utf-8)')
