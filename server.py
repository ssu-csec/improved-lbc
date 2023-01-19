from socket import *
import pickle
import threading
import core
import packet

def Send(client_group, send_data):
	for client in client_group:
		client.sendall(send_data)

def Recv(conn, data):
	while True:
		recv_data = conn.recv(buf)
		mod_info = pickle.loads(recv_data)
		tmp_index = mod_info.modi_index
		tmp_length = mod_info.modi_length
		packet.unpacking(data, mod_info)

port = 8080
buf = 4096

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(3)

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

	
