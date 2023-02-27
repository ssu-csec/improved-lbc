import core
import protocol
#import noneprot										# noneprot
#import exprot											# exprot
import newEditor
from socket import *
from queue import Queue
import curses
import signal
import sys
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
		modi_info.append(str(text))

	return modi_info

raw_key = input("Please write your key: ")
if len(raw_key) > 16:
	raw_key = raw_key[:16]
elif len(raw_key) < 16:
	while len(raw_key) != 16:
		raw_key += '0'

key = core.gen_key(raw_key)
#mode = input("Please choose mode. CTR or CBC? ")					# exprot
#iv = 'Initial Vector 1')											# exprot
tmp_queue = Queue()

flag = [False]

ip_address = input("Input ip address: ")
int(port = input("Input port number: "))

clientSock = socket(AF_INET, SOCK_STREAM)

client = protocol.Client(clientSock, key, tmp_queue, flag)

#client = noneprot.Client(clientSock, tmp_queue)					# noneprot

#client = exprot.Client(clientSock, tmp_queue, mode, raw_key, iv)	# exprot
#port = 8081


client.main(ip_address, port)

signal.signal(signal.SIGINT, handler)
'''
flag = '0'
while flag == '0':
	modi_info = get_modi_info()
	tmp_queue.put(modi_info)
	flag = input("If you want to break, press 0: ")
'''
curses.wrapper(newEditor.main, tmp_queue, flag)

'''
while True:
	try:
		pass
	except KeyboardInterrupt:
		print("Program exit!!")
'''


