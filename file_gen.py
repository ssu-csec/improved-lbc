import random
import pickle
import core

raw_key = "I have a dream!!"
key = core.gen_key(raw_key)

str_len = int(input("Choose file length: "))

f_str = ""

sample_s = "This is an example sentence for our experiments with seventy letters.\n"

for i in range(int(str_len/70)):
	f_str += sample_s
f_str += sample_s[:str_len%70]

data = core.Data()
core.insert(f_str, 0, data, key)
with open("test_server_" + str(str_len) + ".p", 'wb') as f:
	pickle.dump(data, f)

