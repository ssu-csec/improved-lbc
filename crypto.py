from Crypto.Cipher import AES

def CBC_enc(data, key, iv):
	obj = AES.new(key, AES.MODE_CBC, iv)
	cipher = b''
	in_len = len(data)
	while in_len > 16:
		tmp_data = data[:16]
		tmp_cipher = obj.encrypt(tmp_data)
		cipher += tmp_cipher
		in_len -= 16
		data = data[16:]
	
	for i in range(16 - len(data)):
		data += "\0"
	tmp_cipher = obj.encrypt(data)
	cipher += tmp_cipher
	return cipher

def CBC_dec(cipher, key, iv):
	obj = AES.new(key, AES.MODE_CBC, iv)
	data = b''
	in_len = len(cipher)
	print(in_len)
	for i in range(in_len - 1):
		tmp_cipher = cipher[:16]
		tmp_data = obj.decrypt(tmp_cipher)
		data += tmp_data
		cipher = cipher[16:]
	tmp_data = obj.decrypt(cipher)
	num = tmp_data.count(b'\0')
	tmp_data = tmp_data[:(16 - num)]
	data += tmp_data

	return data

def CTR_enc():
	pass

def CTR_dec():
	pass

if __name__ == "__main__":
	key = 'This is a key123'
	iv = 'This is an IV456'
	data = input("Write data: ")
	cipher = CBC_enc(data, key, iv)
	print("ciphertext is ", cipher)

	plain = CBC_dec(cipher, key, iv)

	print("plaintext is ", str(plain))
