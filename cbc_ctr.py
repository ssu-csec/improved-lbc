import aes
import copy

def gen_key(raw_key):
	ascii_key = aes.str2hex(raw_key)
	key_matrix = aes.block2matrix(ascii_key)
	key = aes.key_schedule_Enc(key_matrix)
	return key

class CBC_Crypto:
	def __init__(self, key, initial_vector = None):
		if initial_vector == None:
			self.prev_block = "0123456789abcde"
		else:
			self.prev_block = initial_vector
		self.key = gen_key(key)
	
	def enc_one(self, target):
		prev_data = aes.str2hex(self.prev_block)
		tmp_str = aes.str2hex(target)
		for i in range(16):
			tmp_str[i] = tmp_str[i] ^ prev_data[i]
		enc_matrix = aes.AES_128_Encryption(aes.block2matrix(tmp_str), self.key)
		cipher_block = aes.matrix2block(enc_matrix)
		return cipher_block
	
	def dec_one(self, target):
		plain_block = []
		prev_data = aes.str2hex(self.prev_block)
		dec_block = aes.matrix2block(aes.AES_128_Decryption(aes.block2matrix(target), self.key))
		for i in range(16):
			plain_block.append(dec_block[i] ^ prev_data[i])
		plain_block = aes.hex2str(plain_block)
		return plain_block

	def encrypt(self, plaintext):
		ciphertext = ""
		str_len = len(plaintext)
		for i in range(int(str_len/16)):
			tmp_str = plaintext[:16]
			plaintext = plaintext[16:]
			self.prev_block = self.enc_one(tmp_str)
			ciphertext += ''.join(self.prev_block)
		remain = str_len % 16
		if remain != 0:
			plaintext += "\0"*(16 - remain)
			self.prev_block = self.enc_one(plaintext)
			ciphertext += ''.join(self.prev_block)
		return ciphertext
	
	def decrypt(self, ciphertext):
		plaintext = ""
		str_len = len(ciphertext)
		for i in range(int(str_len/16) - 1):
			tmp_str = ciphertext[:16]
			ciphertext = ciphertext[16:]
			plaintext += ''.join(self.dec_one(tmp_str))
			self.prev_block = tmp_str
		last_block = ''.join(self.dec_one(ciphertext))
		plaintext += last_block.rstrip("\0")
		return plaintext

class CTR_Crypto:
	def __init__(self, key, initial_value = None):
		self.key = gen_key(key)
		if initial_value == None:
			self.iv = aes.str2hex("default ")
		elif len(initial_value) != 8:
			initial_value += initial_value * 7
			self.iv = aes.str2hex(initial_value[:8])
		else:
			self.iv = aes.str2hex(initial_value)
		self.nonce = [0] * 8
	
	def nonceup(self):
		check = -1
		while check > -8:
			if self.nonce[check] > 255:
				self.nonce[check] +=1
				break
			else:
				check -= 1

	def enc_one(self, target):
		cipher_block = []
		nonce = self.iv + self.nonce
		enc_nonce = aes.AES_128_Encryption(aes.block2matrix(nonce), self.key)
		for i in range(len(target)):
			cipher_block.append(aes.str2hex(target)[i] ^ aes.str2hex(aes.matrix2block(enc_nonce))[i])
		self.nonceup
		return cipher_block

	def encrypt(self, plaintext):
		ciphertext = ""
		str_len = len(plaintext)
		for i in range(int(str_len/16)):
			tmp_str = plaintext[:16]
			plaintext = plaintext[16:]
			cipher_block = self.enc_one(tmp_str)
			ciphertext += ''.join(aes.hex2str(cipher_block))
		cipher_block = self.enc_one(plaintext)
		ciphertext += ''.join(aes.hex2str(cipher_block))
		return ciphertext
	
	def decrypt(self, ciphertext):
		plaintext = self.encrypt(ciphertext)
		return plaintext

