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

tmp_queue = Queue()

flag = [False]

clientSock = socket(AF_INET, SOCK_STREAM)


client = noneprot.Client(clientSock, tmp_queue)					

port = int(input("Input port number: "))
ip_address = input("Input ip address: ")

client.main(ip_address, port)

signal.signal(signal.SIGINT, handler)

curses.wrapper(newEditor.main, tmp_queue, flag)



