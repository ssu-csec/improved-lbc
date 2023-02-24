import core
import noneprot			
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

tmp_queue = Queue()

flag = [False]

clientSock = socket(AF_INET, SOCK_STREAM)


client = noneprot.Client(clientSock, tmp_queue)					# noneprot

port = 8081

client.main(port)

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


