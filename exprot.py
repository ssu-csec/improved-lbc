from socket import *
from queue import Queue
import crypto
import pickle
import threading

class Server:
	def __init__(self, port, f_name):
		self.buf = 1024*32
		self.port = port
		self.data = b''
		self.client_group = []
		self.send_queue = Queue()
		self.f_name = f_name

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
				print("client_byebye")
				self.client_group.remove(conn)
				if len(self.client_group) == 0:
					with open(self.f_name, 'wb') as f:
						f.write(self.data)
						f.close
					return
			else:
				self.send_queue.put([conn, recv_data])
				self.data = load_data

	def main(self):
		serverSock = socket(AF_INET, SOCK_STREAM)
		serverSock.bind(('', self.port))
		serverSock.listen(10)
		
		#with open(self.f_name, 'wb') as f:
		#	f.write(self.data)
		#	f.close

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()

		while True:
			connectionSock, addr = serverSock.accept()
			if len(self.client_group) == 0:
				with open(self.f_name, 'rb') as f:
					self.data = f.read()
			self.client_group.append(connectionSock)
			print("Connected to new client", str(addr))
			
			recv_thread = threading.Thread(target = self.Recv, args = (connectionSock, ))
			recv_thread.start()

class Client:
	def __init__(self, sock, input_queue, mode, key, initial_vector):
		self.sock = sock
		self.buf = 1024*32
		self.data = b''
		self.input_queue = input_queue
		self.flag = 0
		self.mode = mode
		self.key = key
		self.iv = initial_vector

	def Modification(self, recv_data):
		plain_data = crypto.Dec(self.mode, self.data, self.key, self.iv)
		if recv_data[0] == "I":
			plain_data = plain_data[:recv_data[1]] + recv_data[2] + plain_data[recv_data[1]:]
		elif recv_data[0] == "D":
			plain_data = plain_data[:recv_data[1]] + plain_data[recv_data[1] + 1:]
		self.data = crypto.Enc(self.mode, plain_data, self.key, self.iv) 

	def Send(self):
		while True:
			while self.flag == 1:
				pass
			modi_data = self.input_queue.get()
			self.Modification(modi_data)
			plain_data = crypto.Dec(self.mode, self.data, self.key, self.iv)
			with open("test.txt", 'w') as f:
				f.write(plain_data)
			self.sock.send(pickle.dumps(self.data))
			self.flag = 1

	def Recv(self):
		while True:
			recv_data = self.sock.recv(self.buf)
			load_data = pickle.dumps(recv_data)
			if load_data == "Success":
				self.flag = 0
			else:
				self.data = load_data
				plain_data = crypto.Dec(self.mode, self.data, self.key, self.iv)
				with open("test.txt", 'w') as f:
					f.write(plain_data)
	
	def main(self, ip_address, port):

		self.sock.connect((ip_address, port))

		recv_data = self.sock.recv(self.buf)
		self.data = pickle.loads(recv_data)
		plain_text = crypto.Dec(self.mode, self.data, self.key, self.iv)
		with open("test.txt", 'w') as f:
			f.write(plain_text)

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()

		recv_thread = threading.Thread(target = self.Recv)
		recv_thread.start()

