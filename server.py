from socket import *
from queue import Queue
import pickle
import random
import threading
import core

class Count:
	def __init__(self):
		self.num = 0

def Conflict_Handling(conflict_list, , send_queue, client_group):
	print("Conflict Handling!")
	flag = 0
	for index in conflict_list[0][1].del_list:
		for comp in conflict_list[1][1].del_list:
			if index == comp:
				flag = 1
				break
	if flag == 1:
		conflict_list[1][0].send(pickle.dumps("Request again"))
		for i in range(len(client_group)):
			if conflict_list[0][0] != client_group[i]:
				client_group[i].send(pickle.dumps(conflic_list[0][1]))
			else:
				sender = i
		client_group[sender].sendall(pickle.dumps("Success"))
	else:
		for data in conflict_list:
			send_queue.put(data)
			#wait(0.01)

def Send(client_group, send_queue):
	while True:
		if send_queue.qsize() > 1:
			conflict_list = []
			while send_queue.empty() == False:
				conflict_list.append(send_queue.get())
			Conflict_Handling(conflict_list, send_queue, client_group)
		recv = send_queue.get()
		if recv == 'Gathering':
			print("send gathering request")
			client_group[random.randint(0, len(client_group) - 1)].send(pickle.dumps('Gathering'))
		elif type(recv[1]) == type([]):
			for i in range(len(client_group)):
				if recv[0] != client_group[i]:
					client_group[i].send(pickle.dumps(recv[1]))
		else:
			for i in range(len(client_group)):
				if recv[0] != client_group[i]:
					client_group[i].send(recv[1])
				else:
					sender = i
			client_group[sender].sendall(pickle.dumps("Success"))

def Recv(conn, data, send_queue, count, client_group): 
	buf = 8196*16
	conn.sendall(pickle.dumps(data))
	while True:
		recv_data = conn.recv(buf)
		modi_info = pickle.loads(recv_data)
		if modi_info == 'EXIT':
			client_group.remove(conn)
			if len(client_group) == 0:
				with open('server_data.p', 'wb') as f:
					pickle.dump(data.f)
					f.close()
		elif type(modi_info) == type([]) and modi_info[0] == 'G':
			send_queue.put([conn, modi_info])
			data.global_meta = modi_info[1].global_meta
			data.data = modi_info[1].data
			count.num -= 10
		else:
			send_queue.put([conn, recv_data])
			count.num += 1
			modi_info.unpacking(data)
		
		if count.num >= 10:
			send_queue.put('Gathering')
		print("get ", count.num, "th data")
	
port = 8080

send_queue = Queue()
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(10)

data = core.Data()
with open("server_data.p", 'wb') as f:
	pickle.dump(data, f)
	f.close()
count = Count()

client_group = []

send_thread = threading.Thread(target = Send, args = (client_group, send_queue, ))
send_thread.start()
while True:
	connectionSock, addr = serverSock.accept()
	if len(client_group) == 0:
		with open("server_data.p", 'rb') as f:
			data.pickle.load(f)
	client_group.append(connectionSock)
	print("Connected to new client ", str(addr))
	recv_thread = threading.Thread(target = Recv, args = (connectionSock, data, send_queue, count, ))
	recv_thread.start()

