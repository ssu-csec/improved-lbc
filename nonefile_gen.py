import random
import pickle

str_len = int(input("Choose file length: "))

f_str = ""

for i in range(str_len):
	asc = random.randint(32, 127)
	f_str += chr(asc)

with open("none_server_" + str(str_len) + ".txt", 'w') as f:
	f.write(f_str)
