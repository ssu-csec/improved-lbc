from socket import *
from queue import Queue
import pickle
import random
import signal
import threading 
import core

def handler(signum, frame):
	global clientSock
	clientSock.sendall(pickle.dumps("EXIT"))
	exit(0)

def get_modify_info(data, key):
	global modi_queue
	modi_info = []
	select = input("Choose Insert(I)/Delete(D): ")
	while select != 'I' and select != 'D':
		if select == 'show':
			dec_str = core.decrypt(data, key)
			print("Plain text", "=" * 80)
			print(*dec_str, sep = '')
			print("")
			print("Global string", "=" * 77)
			print(*core.global_dec(data.global_meta, key), sep = "/")
		print("Please choose right option")
		select = input("Choose Insert(I)/Delete(D): ")
	if select == 'I' or select == 'i':
		plain_data = input("Please write the data you want to insert: ")
		index = int(input("Choose the index: "))
		modi_info = core.insert(plain_data, index, data, key)
		modi_queue.put([index, plain_data])
	elif select == 'D' or select == 'd':
		index = int(input("Choose the index: "))
		modi_info = core.delete(1, index, data, key)
		modi_queue.put([index, -1])
	#print(modi_info)
	return modi_info

def gathering(sock, data, key):
	print("Gathering function start")
	gather_data = core.Data()
	plain = core.decrypt(data, key)
	global_str = core.gen_global(len(plain))
	gather_data.global_meta = core.global_enc(global_str, key)
	iv = random.randint(0,255)
	gather_data.data = core.encrypt(plain, key, iv, iv)
	send_data = pickle.dumps(['G', gather_data])
	sock.sendall(send_data)
	data.global_meta = gather_data.global_meta
	data.data = gather_data.data

def Send(sock, data, key):
	while True:
		modi_info = get_modify_info(data, key)
		send_data = pickle.dumps(modi_info)
		sock.sendall(send_data)

def Recv(sock, data, key):
	global modi_queue
	while True:
		recv_data = sock.recv(buf)
		load_data = pickle.loads(recv_data)
		if load_data == "Gathering":
			print("Gathering request")
			gathering(sock, data, key)
		elif load_data == "Success":
			print("Success!")
			modi_queue.get()
		elif load_data == "Request again":
			request = modi_queue.get()
		elif type(load_data) == type([]) and load_data[0] == 'G':
			data.global_meta = load_data[1].global_meta
			data.data = load_data[1].data
		else:
			#print("Recv data is ", load_data)
			load_data.unpacking(data)

signal.signal(signal.SIGINT, handler)

port = 8080
buf = 8192
raw_key = "python is genius"
key = core.gen_key(raw_key)
clientSock = socket(AF_INET, SOCK_STREAM)

modi_queue = Queue()

data = core.Data()
tmp_index = 0
tmp_length = 0

clientSock.connect(('127.0.0.1', port))

print('connecting')

recv_data = clientSock.recv(buf*4)
load_data = pickle.loads(recv_data)
data.data = load_data.data
data.global_meta = load_data.global_meta
#print("Existing global data is ", data.global_meta, " Existing data is ", data.data)

thread1 = threading.Thread(target = Send, args = (clientSock, data, key, ))
thread1.start()

thread2 = threading.Thread(target = Recv, args = (clientSock, data, key, ))
thread2.start()

