from socket import *
from queue import Queue
import pickle
import random
import signal
import threading 
import time
import core

def handler(signum, frame):
	global clientSock
	clientSock.sendall(pickle.dumps("EXIT"))
	exit(0)

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

def Conflict_Handling(sock, data, key, modi_queue, request):
	recv_data = sock.recv(8196 * 16)
	load_data = pickle.loads(recv_data)
	load_data.unpacking(data)
	if load_data.modi_index <= request[1]:
		request[1] += load_data.modi_length
	modi_queue.put(request)
	if request[0] == 'I':
		modi_info = core.insert(request[2], request[1], data, key)
	elif request[0] == 'D':
		modi_info = core.delete(1, request[1], data, key)
	sock.sendall(pickle.dumps(modi_info))

def Send(sock, data, key, modi_queue, tmp_data):
	while True:
		modi_info = modi_queue.get()
		tmp_data.put(modi_info)
		if modi_info[0] == 'I':
			send_data = core.insert(modi_info[2], modi_info[1], data, key)
		elif modi_info[0] == 'D':
			send_data = core.delete(modi_info[2], modi_info[1], data, key)
		sock.sendall(pickle.dumps(send_data))

def Recv(sock, data, key, tmp_data):
	buf = 8196 * 16
	while True:
		recv_data = sock.recv(buf)
		load_data = pickle.loads(recv_data)
		if load_data == "Gathering":
			print("Gathering request")
			gathering(sock, data, key)
		elif load_data == "Success":
			#print("Success!")
			tmp_data.get()
		elif load_data == "Request again":
			request = tmp_data.get()
			Conflict_Handling(sock, data, key, tmp_data, request)
		elif type(load_data) == type([]) and load_data[0] == 'G':
			data.global_meta = load_data[1].global_meta
			data.data = load_data[1].data
		else:
			#print("Recv data is ", load_data)
			load_data.unpacking(data)

def client_main(port):
	modi_queue = Queue()
	tmp_data = Queue()
	raw_key = "python is genius"
	key = core.gen_key(raw_key)
	global clientSock = socket(AF_INET, SOCK_STREAM)
	signal.signal(signal.SIGINT, handler)
	data = core.Data()
	clientSock.connect(('127.0.0.1', port))
	print('connecting')

	recv_data = clientSock.recv(buf*4)
	load_data = pickle.loads(recv_data)
	data.data = load_data.data
	data.global_meta = load_data.global_meta
	f = open("tmp_data.txt", 'w')
	f.write(''.join(dec))
	f.close

	thread1 = threading.Thread(target = Send, args = (clientSock, data, key, modi_queue, tmp_data, ))
	thread1.start()

	thread2 = threading.Thread(target = Recv, args = (clientSock, data, key, tmp_data, ))
	thread2.start()

	edit.main("tmp_data.txt")

if __name__ == "__main__":
	client_main(8080)
