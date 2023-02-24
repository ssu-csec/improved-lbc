import core
import protocol
import noneprot

port = 8081

server = noneprot.Server(port)	
server.main()

'''
while True:
	try:
		pass
	except KeyboardInterrupt:
		print("server byebye!")
'''

