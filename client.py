from socket import *
import pickle
import random
import threading 
import core
import packet

def get_modify_info(data, key):
	modi_info = []
	select = input("choose Insert(I)/Delete(D): ")
	while select != 'I' and select != 'D':
		if select == 'show':
			dec_str = core.decrypt(data, key)
			print(*dec_str, sep = '')
		print("Please choose right option")
		select = input("choose Insert(I)/Delete(D): ")
	if select == 'I' or select == 'i':
		plain_data = input("Please write the data you want to insert: ")
		index = int(input("Choose the index: "))
		modi_info = core.insert(plain_data, index, data, key)
	elif select == 'D' or select == 'd':
		index = int(input("Choose the index: "))
		modi_info = core.delete(1, index, data, key)
	return modi_info

def gathering(sock, data, key):
	gather_data = core.Data()
	plain = core.decrypt(data, key)
	global_str = core.gen_global(len(plain))
	gather_data.global_meta = global_enc(global_str, key)
	iv = random.randint(0,255)
	gather_data.data = encrypt(plain, key, iv, iv)
	send_data = pickle.dumps(gather_data)
	sock.sendall(send_data)

def Send(sock, data, key):
	while True:
		modi_info = get_modify_info(data, key)
		send_data = pickle.dumps(modi_info)
		sock.sendall(send_data)

def Recv(sock, data, key):
	while True:
		recv_data = sock.recv(buf)
		load_data = pickle.loads(recv_data)
		if recv_data == "Gathering":
			print("Gathering request")
			gathering(sock, data, key)
		else:
			packet.unpacking(data, load_data)

port = 8080
buf = 8192
raw_key = "python is genius"
key = core.gen_key(raw_key)
clientSock = socket(AF_INET, SOCK_STREAM)

data = core.Data()
tmp_index = 0
tmp_length = 0

clientSock.connect(('127.0.0.1', port))

print('connecting')

recv_data = clientSock.recv(buf*4)
load_data = pickle.loads(recv_data)
data.data = load_data.data
data.global_data = load_data.global_meta


thread1 = threading.Thread(target = Send, args = (clientSock, data, key, ))
thread1.start()

thread2 = threading.Thread(target = Recv, args = (clientSock, data, key, ))
thread2.start()

