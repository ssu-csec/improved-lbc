import core
import protocol
import cpedit
from socket import *
from queue import Queue
import signal
import pickle

def handler(signum, frame):
	clientSock.sendall(pickle.dumps("EXIT"))
	exit(0)

def get_modi_info():
	select = ''
	modi_info = []
	while select != "I" and select != "D":
		select = input("Choose Insert(I)/Delete(D): ")
	modi_info.append(select)
	index = input("Choose index: ")
	modi_info.append(int(index))
	if select == "I":
		text = input("Please write what you want to insert: ")
		modi_info.append(text)

	return modi_info

raw_key = input("Please write your key: ")
if len(raw_key) > 16:
	raw_key = raw_key[:16]
elif len(raw_key) < 16:
	while len(raw_key) != 16:
		raw_key += '0'

key = core.gen_key(raw_key)
tmp_queue = Queue()

clientSock = socket(AF_INET, SOCK_STREAM)

client = protocol.Client(clientSock, key, tmp_queue)

port = 8081

client.main(port)

#while True:
signal.signal(signal.SIGINT, handler)
#	modi_info = get_modi_info()
#	tmp_queue.put(modi_info)

cpedit.EditDisplay("test.txt", tmp_queue).main()


