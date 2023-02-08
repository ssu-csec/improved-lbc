from socket import *
from queue import Queue
import pickle
import random
import signal
import threading
import core

class Server:
	def __init__(self, port):
		self.buf = 1024*32
		self.send_queue = Queue()
		self.client_group = []
		self.data = core.Data()
		self.count = 0
		self.port = port

	def Conflict_Handling(self, conflict_list):
		print("Conflict Handling!")
		flag = 0
		for index in conflict_list[0][1].del_list:
			for comp in conflict_list[1][1].del_list:
				if index == comp:
					flag = 1
					break
		if flag == 1:
			conflict_list[1][0].send(pickle.dumps("Request again"))
			for i in range(len(self.client_group)):
				if conflict_list[0][0] != self.client_group[i]:
					self.client_group[i].send(pickle.dumps(conflic_list[0][1]))
				else:
					sender = i
			self.client_group[sender].sendall(pickle.dumps("Success"))
		else:
			for data in conflict_list:
				self.send_queue.put(data)

	def Send(self):
		while True:
			if self.send_queue.qsize() > 1:
				conflict_list = []
				while self.send_queue.empty() == False:
					conflict_list.append(self.send_queue.get())
				Conflict_Handling(self, conflict_list)
			recv = self.send_queue.get()
			if recv == 'Gathering':
				print("send gathering request")
				self.client_group[random.randint(0, len(self.client_group) - 1)].send(pickle.dumps('Gathering'))
			elif type(recv[1]) == type([]):
				for i in range(len(self.client_group)):
					if recv[0] != self.client_group[i]:
						self.client_group[i].send(pickle.dumps(recv[1]))
			else:
				for i in range(len(self.client_group)):
					if recv[0] != self.client_group[i]:
						self.client_group[i].send(recv[1])
					else:
						sender = i
				self.client_group[sender].sendall(pickle.dumps("Success"))
	
	def Recv(self, conn): 
		conn.sendall(pickle.dumps(data))
		while True:
			recv_data = conn.recv(self.buf)
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
				self.count -= 10
			else:
				send_queue.put([conn, recv_data])
				self.count += 1
				modi_info.unpacking(data)
		
			if self.count >= 10:
				self.send_queue.put('Gathering')
			print("get ", self.count, "th data")
	def main(self):
		serverSock = socket(AF_INET, SOCK_STREAM)
		serverSock.bind(('', self.port))
		serverSock.listen(10)

		with open("server_data.p", 'wb') as f:
			pickle.dump(self.data, f)
			f.close()

		send_thread = threading.Thread(target = self.Send, args = (self, ))
		send_thread.start()
		while True:
			connectionSock, addr = serverSock.accept()
			if len(self.client_group) == 0:
				with open("server_data.p", 'rb') as f:
					self.data.pickle.load(f)
			self.client_group.append(connectionSock)
			print("Connected to new client ", str(addr))
			recv_thread = threading.Thread(target = self.Recv, args = (self, connectionSock, ))
			recv_thread.start()

class Client:
	def __init__(self, sock, key, input_queue):
		self.buf = 1024*32
		self.sock = sock
		self.data = core.Data()
		self.key = key
		self.input_queue = input_queue
		self.tmp_data = []
		self.flag = 0
		
	def gathering(self):
		plain = core.decrypt(self.data, self.key)
		global_str = core.gen_global(len(plain))
		self.data.global_meta = core.global_enc(global_str, key)
		iv = random.randint(0,255)
		self.data.data = core.encrypt(plain, key, iv, iv)
		self.sock.sendall(pickle.dumps(['G', self.data]))
	
	def Conflict_Handling(self, request)
		recv_data = self.sock.recv(self.buf)
		load_data = pickle.loads(recv_data)
		load_data.unpacking(self.data)
		if load_data.modi_index <= request[1]:
			request[1] += load_data.modi_length
		self.input_queue.put(request)
		self.tmp_data = request
		self.flag = 1
	
	def Send(self):
		while True:
			while flag == 1:
				pass
			modi_info = self.input_queue.get()
			self.tmp_data = modi_info
			if modi_info[0] == "I":
				send_data = core.insert(modi_info[2], modi_info[1], self.data, self.key)
			elif modi_info == "D":
				send_data = core.delete(1, modi_info[1], self.data, self.key)
			self.sock.sendall(pickle.dumps(send_data))
			self.flag = 1
	
	def Recv(self):
		while True:
			recv_data = self.sock.recv(self.buf)
			load_data = pickle.loads(recv_data)
			if load_data == "Gathering"
				print("Gathering request")
				self.gathering()
			elif load_data == "Success":
				self.flag = 0
				self.tmp_data = []
			elif load_data == "Request again":
				self.Conflict_Handling(self, self.tmp_data)
			elif type(load_data) == type([]) and load_data[0] == "G":
				self.data.global_meta = load_data[1].global_meta
				self.data.data = load_data[1].data
			else:
				load_data.unpacking(self.data)
	def main(self, port):
		
		self.sock.connect(("127.0.0.1", port))

		recv_data = self.sock.recv(self.buf)
		load_data = pickle.loads(recv_data)
		self.data = load_data

		send_thread = threading.Thread(target = self.Send, args = (self, ))
		send_thread.start()

		recv_thread = threading.Thread(target = self.Recv, args = (self, ))
		recv_thread.start()

