import cbc_ctr

def Enc(mode, data, key, iv):
	if mode == "CBC":
		obj = cbc_ctr.CBC_Crypto(key, iv)
	elif mode == "CTR":
		obj = cbc_ctr.CTR_Crypto(key, iv)
	
	cipher = obj.encrypt(data)

	return cipher

def Dec(mode, cipher, key, iv):
	if mode == "CBC":
		obj = cbc_ctr.CBC_Crypto(key, iv)
	elif mode == "CTR":
		obj = cbc_ctr.CTR_Crypto(key, iv)
	
	plain = obj.decrypt(cipher)

	return plain

if __name__ == "__main__":
	key = 'This is a key123'
	iv = 'This is an IV456'
	mode = input("Choose mode CBC or CTR? ")
	data = input("Write data: ")
	cipher = Enc(mode, data, key, iv)
	print("ciphertext is ", cipher)

	plain = Dec(mode, cipher, key, iv)

	print("plaintext is '", plain, "'")
