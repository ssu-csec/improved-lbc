from socket import *
import pickle 
import core
import packet

def get_modify_info(data, key):
	select = input("choose Insert(I)/Delete(D): ")
	if select == 'I':
		plain_data = input("Please write the data you want to insert: ")
		index = int(input("Choose the index: "))
		modi_info = core.insert(plain_data, index, data, key)
	elif select == 'D':
		index = int(input("Choose the index: "))
		modi_info = core.delete(1, index, data, key)
	else:
		print("Please choose right options")
	return modi_info

port = 8081
buf = 1024
raw_key = "python is genius"
key = core.gen_key(raw_key)
clientSock = socket(AF_INET, SOCK_STREAM)

data = core.Data()
tmp_index = 0
tmp_length = 0

clientSock.connect(('127.0.0.1', port))

print('connecting')

while True:
	
	recv_data = clientSock.recv(buf)
	load_data = pickle.loads(recv_data)
	packet.unpacking(data, load_data)
	modi_info = get_modify_info(data, key)
	send_data = pickle.dumps(modi_info)
	clientSock.sendall(send_data)
	
