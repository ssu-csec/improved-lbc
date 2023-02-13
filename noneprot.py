from socket import *
from queue import Queue
import pickle
import threading

class Server:
	def __init__(self, port):
		self.port = port
		self.buf = 1024*8
		self.client_group = []
		self.send_queue = Queue()
		self.data = []

	def Modification(self, recv_data):
		if recv_data[0] == "I":
			self.data = self.data[:recv_data[1]] + recv_data[2] + self.data[recv_data[1]:]

		elif recv_data[0] == "D":
			self.data = self.data[:recv_data[1]] + self.data[recv_data[1] + 1:]

	def Send(self):
		while True:
			recv = self.send_queue.get()
			for i in range(len(self.client_group)):
				if recv[0] != self.client_group[i]:
					self.client_group[i].send(recv[1])
				else:
					sender = i
			self.client_group[sender].send(pickle.dumps("Success"))

	def Recv(self, conn):
		conn.sendall(pickle.dumps(self.data))
		while True:
			recv_data = conn.recv(self.buf)
			load_data = pickle.loads(recv_data)
			if load_data == "EXIT":
				print("Client byebye")
				self.client_group.remove(conn)
				if len(self.client_group) == 0:
					data_str = ''.join(str(s) for s in self.data)
					with open("none_data.txt", "w") as f:
						f.write(data_str)
						f.close
					return
			else:
				self.send_queue.put([conn, recv_data])
				self.Modification(load_data)
	
	def main(self):
		serverSock = socket(AF_INET, SOCK_STREAM)
		serverSock.bind(('', self.port))
		serverSock.listen(10)
		
		data_str = ''.join(str(s) for s in self.data)
		with open("none_data.txt", 'w') as f:
			f.write(data_str)
			f.close()

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()

		while True:
			connectionSock, addr = serverSock.accept()
			if len(self.client_group) == 0:
				with open("none_data.txt", 'r') as f:
					self.data = f.read()
			self.client_group.append(connectionSock)
			print("Connected to new client ", str(addr))
			recv_thread = threading.Thread(target = self.Recv, args = (connectionSock, ))
			recv_thread.start()

class Client:
	def __init__(self, sock, input_queue):
		self.sock = sock
		self.buf = 1024*8
		self.data = []
		self.input_queue = input_queue
		self.flag = 0

	def Modification(self, recv_data):
		if recv_data[0] == 'I':
			self.data = self.data[:recv_data[1]] + recv_data[2] + self.data[recv_data[1]:]
		elif recv_data[1] == "D":
			self.data = self.data[:recv_data[1]] + self.data[recv_data[1] + 1:]

	def Send(self):
		while True:
			while self.flag == 1:
				pass
			modi_data = self.input_queue.get()
			self.sock.send(pickle.dumps(modi_data))
			self.flag = 1
			self.Modification(modi_data)
			
	def Recv(self):
		while True:
			recv_data = self.sock.recv(self.buf)
			load_data = pickle.loads(recv_data)
			if load_data == "Success":
				self.flag = 0
			else:
				self.Modification(load_data)

	def main(self, port):
		
		self.sock.connect(("127.0.0.1", port))

		recv_data = self.sock.recv(self.buf)
		load_data = pickle.loads(recv_data)
		self.data = load_data

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()

		recv_thread = threading.Thread(target = self.Recv)
		recv_thread.start()
						
