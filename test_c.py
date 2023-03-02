import core
import protocol
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

raw_key = input("Please write your key: ")
if len(raw_key) > 16:
	raw_key = raw_key[:16]
elif len(raw_key) < 16:
	while len(raw_key) != 16:
		raw_key += '0'

key = core.gen_key(raw_key)
tmp_queue = Queue()

port = int(input("Input port number: "))
ip_address = input("Input ip address: ")

clientSock = socket(AF_INET, SOCK_STREAM)

client = protocol.Client(clientSock, key, tmp_queue)

client.main(ip_address, port)

signal.signal(signal.SIGINT, handler)
curses.wrapper(newEditor.main, tmp_queue)


