from socket import *
from queue import Queue
import pickle
import random
import threading
import core
import packet

def Send(client_group, send_queue):
	while True:
		recv = send_queue.get()
		print("receive data is ", recv)
		if recv == 'new client':
			break
		if recv == 'Gathering':
			client_group[random.randint(0, len(client_group) - 1)].send(pickle.dumps('Gathering'))
		else:
			print("check point1")
			for client in client_group:
				if recv[0] != client:
					client.send(recv[1])

def Recv(conn, data, send_queue, cnt):
	while True:
		recv_data = conn.recv(buf)
		send_queue.put([conn, recv_data])
		cnt += 1
		mod_info = pickle.loads(recv_data)
		packet.unpacking(data, mod_info)
		if cnt >= 20:
			send_queue.put('Gathering')
			cnt -= 20
		print("get ", cnt, "th data")

port = 8080
buf = 8192

send_queue = Queue()
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(10)

data = core.Data()
tmp_index = 0
tmp_length = 0
cnt = 0

client_group = []

while True:
	connectionSock, addr = serverSock.accept()
	client_group.append(connectionSock)
	print("Connected to new client ", str(addr))
	send_data = pickle.dumps(data)
	connectionSock.sendall(send_data)

	send_queue.put('new client')
	send_thread = threading.Thread(target = Send, args = (client_group, send_queue, ))
	send_thread.start()

	recv_thread = threading.Thread(target = Recv, args = (connectionSock, data, send_queue, cnt, ))
	recv_thread.start()

	
