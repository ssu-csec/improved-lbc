from Crypto.Cipher import AES
from Crypto.Util import Counter

def Enc(mode, data, key, iv):
	if mode == "CBC":
		obj = AES.new(key, AES.MODE_CBC, iv)
	elif mode == "CTR":
		counter_obj = Counter.new(128, initial_value = iv[-1])
		obj = AES.new(key, AES.MODE_CTR, counter = counter_obj)
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

def Dec(mode, cipher, key, iv):
	if mode == "CBC":
		obj = AES.new(key, AES.MODE_CBC, iv)
	elif mode == "CTR":
		counter_obj = Counter.new(128, initial_value = iv[-1])
		obj = AES.new(key, AES.MODE_CTR, counter = counter_obj)
	data = b''
	in_len = len(cipher)
	#print(in_len)
	for i in range(in_len - 1):
		tmp_cipher = cipher[:16]
		tmp_data = obj.decrypt(tmp_cipher)
		data += tmp_data
		cipher = cipher[16:]
	tmp_data = obj.decrypt(cipher)
	#num = tmp_data.count(b'\x00')
	#print("num : ", num)
	#tmp_data = tmp_data[:(16 - num)]
	data += tmp_data

	return str(data.rstrip(b"\x00"))[2:-1]

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
