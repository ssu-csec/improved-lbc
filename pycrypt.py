import pyaes

def Enc(mode, data, raw_key, iv):
	key = bytes(raw_key, 'utf-8')
	if mode == "CBC":
		obj = pyaes.AESModeOfOperationCBC(key, iv = iv)	
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
	elif mode == "CTR":
		counter = pyaes.Counter(initial_value = int(iv[-1]))
		obj = pyaes.AESModeOfOperationCTR(key, counter = counter)
		cipher = obj.encrypt(data)
	return cipher

def Dec(mode, cipher, raw_key, iv):
	key = bytes(raw_key, 'utf-8')
	#print("the length of ciphertext is ", len(cipher), ", also the type of ciphertext is ", type(cipher))
	if mode == "CBC":
		obj = pyaes.AESModeOfOperationCBC(key, iv = iv)
		plain = b''
		in_len = int(len(cipher)/16)
		print("in_len = ", in_len)
		for i in range(in_len - 1):
			tmp_cipher = cipher[:16]
			tmp_data = obj.decrypt(tmp_cipher)
			plain += tmp_data
			cipher = cipher[16:]
		tmp_data = obj.decrypt(cipher)
		num = tmp_data.count(b'\00')
		tmp_data = tmp_data[:(16 - num)]
		plain += tmp_data

	elif mode == "CTR":
		counter = pyaes.Counter(initial_value = int(iv[-1]))
		obj = pyaes.AESModeOfOperationCTR(key, counter = counter)
		plain = obj.decrypt(cipher)

	return plain
#	return str(data.rstrip(b"\x00"))[2:-1]

if __name__ == "__main__":
	key = 'This is a key123'
	iv = 'This is an IV456'
	mode = input("Choose mode CBC or CTR? ")
	data = input("Write data: ")
	cipher = Enc(mode, data, key, iv)
	print("ciphertext is ", cipher)

	plain = Dec(mode, cipher, key, iv)

	print("plaintext is ", plain)
	print(plain)
