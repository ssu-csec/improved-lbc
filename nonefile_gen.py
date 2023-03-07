import random
import pickle

str_len = int(input("Choose file length: "))

f_str = ""

sample_s = "It is a sample sentence for test with 50 letters.\n"

for i in range(int(str_len/50)):
	f_str += sample_s
f_str += sample_s[:str_len%50]

with open("none_server_" + str(str_len) + ".txt", 'w') as f:
	f.write(f_str)

