import random
import pickle
import crypto

key = "I have a dream!!"
iv = 'Initial Vector 2'
mode = input("Choose mode. CTR or CBC?: ")
str_len = int(input("Choose file length: "))

f_str = ""


sample_s = "This is an example sentence for our experiments with seventy letters.\n"

for i in range(int(str_len/70)):
	f_str += sample_s
f_str += sample_s[:str_len%70]

data = crypto.Enc(mode, f_str, key, iv)
with open("ex_server_" + str(str_len) + "_" + mode + ".p", 'w') as f:
	f.write(data)

