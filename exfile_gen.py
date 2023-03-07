import random
import pickle
#import crypto
import modes

key = "I have a dream!!"
iv = 'Initial Vector 1'
mode = input("Choose mode. CTR or CBC?: ")
str_len = int(input("Choose file length: "))

f_str = ""


sample_s = "it is a sample sentence for test with 50 letters.\n"

for i in range(int(str_len/50)):
	f_str += sample_s
f_str += sample_s[:str_len%50]

data = modes.Enc(mode, f_str, key, iv)
with open("ex_server_" + str(str_len) + "_" + mode + ".p", 'w') as f:
	f.write(data)

