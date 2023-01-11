import core
import aes
import random

data = input("type any string: ")
key = 'python3 aes keys'

ascii_key = aes.str2hex(key)
key_matrix = aes.block2matrix(ascii_key)
print(key_matrix)

global_meta = []
rkey = aes.key_schedule_Enc(key_matrix)
print("=" * 89)
print("encrypted")
print("")
enc_data = []
enc_data = core.insert(data, 0, enc_data, rkey, global_meta)
print(enc_data)
print("")
print("=" * 89)
print("global_meta")
print(global_meta)
print("")
print("=" * 89)
ins = input("type more: ")
index = int(input("choose index: "))
added_data = core.insert(ins, index, enc_data, rkey, global_meta)
print("decrypted")
print("")
dec_str = core.decrypt(added_data, rkey, global_meta)
print(dec_str)
print("=" * 89)
print("")
print("plain text")
plain = []
for char in dec_str:
	plain.append(chr(char))
print(*plain, sep = '')
print("")



