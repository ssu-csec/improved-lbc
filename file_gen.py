import random
import pickle
import core

raw_key = "I have a dream!!"
key = core.gen_key(raw_key)

str_len = int(input("Choose file length: "))

f_str = ""

for i in range(str_len):
	if i%50 == 0:
		f_str += "\n"
	else:
		asc = random.randint(32, 127)
		f_str += chr(asc)

data = core.Data()
core.insert(f_str, 0, data, key)
with open("test_server_" + str(str_len) + ".p", 'wb') as f:
	pickle.dump(data, f)

