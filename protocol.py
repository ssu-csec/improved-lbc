from socket import *
from queue import Queue
import pickle
import random
import threading
import aes
import core
import time

class Server:
	def __init__(self, port, f_name):
		self.buf = 1024**3
		self.send_queue = Queue()
		self.client_group = []
		self.data = core.Data()
		self.count = 0
		self.port = port
		self.f_name = f_name

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
				self.Conflict_Handling(self, conflict_list)
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
		conn.sendall(pickle.dumps(self.data))
		while True:
			recv_data = conn.recv(self.buf)
			modi_info = pickle.loads(recv_data)
			if modi_info == 'EXIT':
				print("Client byebye")
				self.client_group.remove(conn)
				if len(self.client_group) == 0:
					with open(self.f_name, 'wb') as f:
						pickle.dump(self.data, f)
					return
			elif type(modi_info) == type([]) and modi_info[0] == 'G':
				self.send_queue.put([conn, modi_info])
				self.data.global_meta = modi_info[1].global_meta
				self.data.data = modi_info[1].data
				self.count -= 10
			else:
				self.send_queue.put([conn, recv_data])
				self.count += 1
				modi_info.unpacking(self.data)
				#print("Now Data is ", self.data.data)
				print("get ", self.count, "th data")
		
			if self.count >= 10:
				self.send_queue.put('Gathering')
	def main(self):
		serverSock = socket(AF_INET, SOCK_STREAM)
		serverSock.bind(('', self.port))
		serverSock.listen(10)

		#with open("server_data.p", 'wb') as f:
		#	pickle.dump(self.data, f)
		#	f.close()

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()
		while True:
			connectionSock, addr = serverSock.accept()
			if len(self.client_group) == 0:
				with open(self.f_name, 'rb') as f:
					self.data = pickle.load(f)
			self.client_group.append(connectionSock)
			print("Connected to new client ", str(addr))
			recv_thread = threading.Thread(target = self.Recv, args = (connectionSock, ))
			recv_thread.start()

class Client:
	def __init__(self, sock, key, input_queue):
		self.buf = 1024**3
		self.sock = sock
		self.data = core.Data()
		self.key = key
		self.input_queue = input_queue
		self.tmp_data = []
		self.flag = 0
		
	def gathering(self):
		plain = core.decrypt(self.data, self.key)
		global_str = core.gen_global(len(plain))
		self.data.global_meta = core.global_enc(global_str, self.key)
		iv = random.randint(0,255)
		self.data.data = core.encrypt(plain, self.key, iv, iv)
		self.sock.sendall(pickle.dumps(['G', self.data]))
	
	def Conflict_Handling(self, request):
		recv_data = self.sock.recv(self.buf)
		load_data = pickle.loads(recv_data)
		load_data.unpacking(self.data)
		if load_data.modi_index <= request[1]:
			request[1] += load_data.modi_length
		self.input_queue.put(request)
		self.tmp_data = request
		self.flag = 1
	
	def file_update(self, f_name, modi_info):
		with open(f_name, 'r') as f:
			f_data = f.read()
		if type(modi_info) == type([]):				# modify inside
			if modi_info[0] == "I":
				f_data = f_data[:modi_info[1]] + modi_info[2] + f_data[modi_info[1]:]
			elif modi_info[0] == "D":
				f_data = f_data[:modi_info[1]] + f_data[modi_info[1] + 1:]

		else:										# modify outside
			global_str = core.global_dec(self.data.global_meta, self.key)
			del_len = 0
			for del_index in modi_info.del_list:
				del_len += global_str[del_index]
			del_start = 0
			if len(modi_info.del_list) != 0:
				for pre_index in range(modi_info.del_list[-1]):
					del_start += global_str[pre_index]
			f_data = f_data[:del_start] + f_data[del_start + del_len:]
			global_str = core.global_dec(modi_info.glob_list, self.key)
			ins_data = ''
			ins_index = modi_info.ins_list[0]
			back_link = 0
			for ins_block in modi_info.ins_list[1:]:
				dec_block = core.dec_one(ins_block, self.key, back_link, ins_index)
				back_link = dec_block.pop()
				dec_block = dec_block[:global_str[ins_index]]
				ins_data += ''.join(aes.hex2str(dec_block))
				ins_index += 1
			f_data = f_data[:del_start] + ins_data + f_data[del_start:]
		with open("test.txt", 'w') as f:
			f.write(f_data)

	def Send(self):
		start = 0
		end = 0
		time_i = 0
		while True:
			while self.flag == 1:
				pass
			end = time.time()				#time check end2
			with open("time_check.txt", 'a') as f:
				tmp_str = str(time_i) + " : " + str(end - start) + "\n"
				f.write(tmp_str)
				time_i += 1
			modi_info = self.input_queue.get()
			start = time.time()				#time check start
			self.tmp_data = modi_info
			#send_data = core.Modi_list(0,0)
			#print("tmp data is ", self.tmp_data)
			self.file_update("test.txt", modi_info)
			if modi_info[0] == "I":
				send_data = core.insert(modi_info[2], modi_info[1], self.data, self.key)
			elif modi_info[0] == "D":
				send_data = core.delete(1, modi_info[1], self.data, self.key)
				#Debug
			'''
			plainDebug = core.decrypt(self.data, self.key)
			with open("./Debug.txt", "a") as f:
				f.write(str(modi_info))
				f.write("\n")
				f.write(''.join(plainDebug))
				f.write("\n==========\n")
			'''
			self.sock.sendall(pickle.dumps(send_data))
			self.flag = 1
	
	def Recv(self):
		while True:
			recv_data = self.sock.recv(self.buf)
			load_data = pickle.loads(recv_data)
			if load_data == "Gathering":
				#print("Gathering request")
				self.gathering()
			elif load_data == "Success":
				#time check end1
				self.flag = 0
				self.tmp_data = []
			elif load_data == "Request again":
				self.Conflict_Handling(self, self.tmp_data)
			elif type(load_data) == type([]) and load_data[0] == "G":
				self.data.global_meta = load_data[1].global_meta
				self.data.data = load_data[1].data
			else:
				self.outer_flag[0] = True
				self.file_update("test.txt", load_data)
				load_data.unpacking(self.data)
	
	def main(self, ip_address, port):
		
		self.sock.connect((ip_address, port))

		recv_data = self.sock.recv(self.buf)
		load_data = pickle.loads(recv_data)
		self.data = load_data
		plain_text = core.decrypt(self.data, self.key)
		with open("test.txt", 'w') as f:
			f.write(''.join(plain_text))

		send_thread = threading.Thread(target = self.Send)
		send_thread.start()

		recv_thread = threading.Thread(target = self.Recv)
		recv_thread.start()

