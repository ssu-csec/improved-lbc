import core
import protocol
#import noneprot								# noneprot
#import exprot									# exprot

#port = 8081

port = int(input("Input port number: "))
server = protocol.Server(port)
#server = noneprot.Server(port)					# noneprot
#server = exprot.Server(port)					# exprot
server.main()

'''
while True:
	try:
		pass
	except KeyboardInterrupt:
		print("server byebye!")
'''

