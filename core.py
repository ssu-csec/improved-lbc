import random
import aes
import copy

one_block_len = 14

class Data:
	def __init__(self):
		self.global_meta = []
		self.data = []

class Modi_list:
	def __init__(self, index, length):
		self.modi_index = index
		self.modi_length = length
		self.glob_list = []
		self.del_list = []
		self.ins_inst = []

def gen_key(raw_key):
	ascii_key = aes.str2hex(raw_key)
	key_matrix = aes.block2matrix(ascii_key)
	key = aes.key_schedule_Enc(key_matrix)
	return key

def enc_one(input_str, enc_key, f_link, b_link):		# input_str: int list / enc_key : round key list / f_iv : int type / b_link : int type
	input_block = [f_link]
	input_block.extend(input_str)
	input_block.append(b_link)
	plain_block = aes.block2matrix(input_block)
	output_matrix = aes.AES_128_Encryption(plain_block, enc_key)
	return output_matrix

def dec_one(input_matrix, dec_key, back_link, i):
	out_str = []
	out_matrix = aes.AES_128_Decryption(input_matrix, dec_key)
	for out_row in out_matrix:
		out_str.extend(out_row)
	if back_link != out_str.pop(0) and back_link != 0:
		print("There is something wrong in block number", i)
		out_str[14] = 0
	return out_str

def gen_global(str_len):
	global_str = []
	left_len = str_len
	while left_len > one_block_len:
		global_str.append(one_block_len)
		left_len -= one_block_len
	global_str.append(left_len)
	return global_str

def global_enc(input_str, enc_key):
	block = []
	output_list = []
	front_link = random.randint(0,255)
	back_link = random.randint(0, 255)
	i = 0
	left_len = len(input_str)
	for char in input_str:
		i += 1
		block.append(char)
		left_len -= 1
		if i == one_block_len and left_len != 0:
			enc_block = enc_one(block, enc_key, front_link, back_link)
			output_list.append(enc_block)
			block = []
			i = 0
			front_link = back_link
			back_link = random.randint(0,255)
		elif left_len == 0:
			remain = one_block_len - i
			for j in range(remain):
				block.append(0)
			enc_block = enc_one(block, enc_key, front_link, back_link)
			output_list.append(enc_block)
	return output_list

def global_dec(input_list, dec_key):
	output_str = []
	back_link = 0
	i = 0
	if len(input_list) == 0:
		return output_str
	for input_matrix in input_list:
		dec_str = dec_one(input_matrix, dec_key, back_link, i)
		back_link = dec_str.pop()
		output_str.extend(dec_str)
		i += 1
	return output_str

def encrypt(input_str, enc_key, f_iv, b_iv):		# input_str: string / enc_key : round key list / f_iv, b_link : int type /
	output_list = []
	input_hex = []
	left_len = len(input_str)
	front_link = f_iv
	back_link = random.randint(0,255)
	input_hex = aes.str2hex(input_str)
	i = 0
	block = []
	block_list = []
	for char in input_hex:
		i += 1
		block.append(char)
		left_len -= 1
		if i == one_block_len and left_len != 0:
			enc_block = enc_one(block, enc_key, front_link, back_link)
			block_list.append(enc_block)
			block = []
			i = 0
			front_link = back_link
			back_link = random.randint(0,255)
		elif left_len == 0:
			remain = one_block_len - i
			for j in range(remain):
				block.append(0)
			enc_block = enc_one(block, enc_key, front_link, b_iv)
			block_list.append(enc_block)
			block = []
	return block_list

def decrypt(input_data, dec_key):
	output_str = []
	back_link = 0
	i = 0
	global_str = global_dec(input_data.global_meta, dec_key)
	for enc_matrix in input_data.data:
		dec_str = dec_one(enc_matrix, dec_key, back_link, i)
		back_link = dec_str.pop()
		for j in range(global_str[i]):
			output_str.append(dec_str[j])
		i += 1
	return output_str

def search_block_index(global_str, index):
	check = index
	block_index = 0
	while check > 0:
		check -= global_str[block_index]
		block_index += 1
	if check < 0:
		block_index -= 1
	
	return block_index

def insert(insert_str, index, input_data, key):
	output_list = Modi_list(index, len(insert_str))
	global_str = global_dec(input_data.global_meta, key)
	new_glob_str = []
	if index == 0 and len(global_str) == 0:
		in_index = index
		block_index = 0
		f_link = random.randint(0,255)
		b_link = f_link	
	else:
		index -= 1
		in_index = index
		block_index = search_block_index(global_str, index)
		for i in range(block_index):
			in_index -= global_str[i]
		if in_index == 0:
			tmp_matrix = aes.AES_128_Decryption(input_data.data[block_index], key)
			f_link = tmp_matrix[3][3]
			tmp_matrix = aes.AES_128_Decryption(input_data.data[block_index], key)
			b_link = tmp_matrix[0][0]
		else:
			tmp_matrix = aes.AES_128_Decryption(input_data.data[block_index], key)
			tmp_hex = aes.matrix2block(tmp_matrix)
			output_list.del_list.append(block_list)				# for networking
			del input_data.data[block_index]
			del global_str[block_inddex]
			f_link = tmp_hex.pop(0)
			b_link = tmp_hex.pop()
			tmp_str = aes.hex2str(tmp_hex)
			insert_list = list(insert_str)
			insert_str = tmp_str[:in_index] + insert_list + tmp_str[in_index:global_str[block_index]]

	insert_list = encrypt(insert_str, key, f_link, b_link)
	new_global_str = gen_global(len(insert_str))
	global_str = global_str[:block_index] + new_global_str + global_str[block_index:]
	input_data.global_meta = global_enc(global_str, key)
	output_list.glob_list.append(input_data.global_meta)		# for networking
	output_list.ins_list.append(block_index)					# for networking
	output_list.ins_list.extend(insert_list)					# for networking
	input_data.data = input_data.data[:block_index] + insert_list + input_data.data[block_index:]
	
	return output_list

def delete(del_len, index, input_data, key):
	output_list = Modi_list(index, -(del_len))
	global_str = global_dec(input_data.global_meta, key)
	index -= 1
	block_index = search_block_index(global_str, index)
	in_index = index
	for i in range(block_index):
		in_index -= global_str[i]
	if del_len == 1:			# delete one letter per one time
		if global_str[block_index] == 1:	# remove one block
			if block_index == 0:
				tmp_block = aes.AES_128_Decryption(input_data.data[len(input_data.data) - 1], key)
				f_link = tmp_block[3][3]
				tmp_block = aes.AES_128_Decryption(input_data.data[block_index + 1], key)
				tmp_block[0][0] = f_link
				tmp_block = aes.AES_128_Encryption(tmp_block, key)
				output_list.del_list.append(block_list + 1)		# for networking
				output_list.del_list.append(block_list)			# for networking
				del input_data.data[block_index]
				del input_data.data[block_index]
				output_list.ins_list.append(block_index)		# for networking
				output_list.ins_list.append(tmp_block)			# for networking
				input_data.data.insert(block_index, tmp_block)
			else:
				new_link = random.randint(0, 255)
				front_block = aes.AES_128_Decryption(input_data.data[block_index - 1], key)
				front_block[3][3] = new_link
				front_block = aes.AES_128_Encryption(front_block, key)
				back_block = aes.AES_128_Decryption(input_data.data[block_index + 1], key)
				back_block[0][0] = new_link
				back_block = aes.AES_128_Encryption(back_block, key)
				output_list.del_list.extend([block_index + 1, block_index, block_index - 1])	# for networking
				del input_data.data[block_index - 1]
				del input_data.data[block_index - 1]
				del input_data.data[block_index - 1]
				output_list.ins_list.append(block_index - 1)	# for networking		
				output_list.ins_list.extend([front_block, back_block])							# for networking
				input_data.data.insert(block_index - 1, front_block)
				input_data.data.insert(block_index, back_block)
			del global_str[block_index]
		else:							# remove one letter in the block
			tmp_block = aes.AES_128_Decryption(input_data.data[block_index], key)
			tmp_str = aes.matrix2block(tmp_block)
			del tmp_str[in_index + 1]
			tmp_str.insert(14, 0)
			tmp_block = aes.block2matrix(tmp_str)
			tmp_block = aes.AES_128_Encryption(tmp_block, key)
			output_list.del_list.append(block_index)			# for networking
			del input_data.data[block_index]
			output_list.ins_list.append(block_index)			# for networking
			output_list.ins_list.append(tmp_block)				# for networking
			input_data.data.insert(block_index, tmp_block)
			global_str[block_index] -= 1
		input_data.global_meta = global_enc(global_str, key)
		output_list.glob_list = input_data.global_meta

	return output_list
