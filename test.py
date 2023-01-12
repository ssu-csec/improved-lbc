import core
import aes
import random

#data = input("type any string: ")
key = input("type 16 byte string for key: ")

ascii_key = aes.str2hex(key)
key_matrix = aes.block2matrix(ascii_key)
rkey = aes.key_schedule_Enc(key_matrix)

global_meta = []
data = []

select = input("choose Insert(I)/Delete(D)/Quit(Q): ")
while select != 'Q':
	if select == 'I':
		plain_data = input("Please write the data you want to insert: ")
		index = int(input("Choose the index: "))
		data = core.insert(plain_data, index, data, rkey, global_meta)
	elif select == 'D':
		index = int(input("Choose the index: "))
		data = core.delete(1, index, data, rkey, global_meta)
	else:
		print("Please choose right options")
	select = input("choose Insert(I)/Delete(D)/Quit(Q): ")

dec_str = core.decrypt(data, rkey, global_meta)
plain = []
for char in dec_str:
	plain.append(chr(char))
print(*plain, sep = '')
"""
enc_data = core.insert(data, 0, enc_data, rkey, global_meta)
print("=" * 89)
ins = input("type more: ")
index = int(input("choose index: "))
added_data = core.insert(ins, index, enc_data, rkey, global_meta)
dec_str = core.decrypt(added_data, rkey, global_meta)
print("=" * 89)
print("")
print("plain text")
plain = []
for char in dec_str:
	plain.append(chr(char))
print(*plain, sep = '')
print("")
"""


