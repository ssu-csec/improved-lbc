from socket import *
import pickle
import core
import packet

port = 8081
buf = 1024

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

data = core.Data()
tmp_index = 0
tmp_length = 0

connectionSock, addr = serverSock.accept()

print('connecting success from port number', port)

send_data = pickle.dumps(data)
connectionSock.sendall(send_data)

while True:
	
	recv_data = connectionSock.recv(buf)
	connectionSock.sendall(recv_data)
	mod_info = pickle.loads(recv_data)
	print("recv_data is ", mod_info)
	tmp_index = mod_info.modi_index
	tmp_length = mod_info.modi_length
	packet.unpacking(data, mod_info)

	
