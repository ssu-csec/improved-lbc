import random
import pickle
import crypto

key = "I have a dream!!"
iv = 'Initial Vector 1'
mode = input("Choose mode. CTR or CBC?: ")
str_len = int(input("Choose file length: "))

f_str = ""

for i in range(str_len):
	if i%50 == 0:
		f_str += "\n"
	else:
		asc = random.randint(32, 127)
		f_str += chr(asc)

data = crypto.Enc(mode, f_str, key, iv)
with open("ex_server_" + str(str_len) + "_" + mode + ".p", 'wb') as f:
	f.write(data)

