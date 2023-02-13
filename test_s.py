import core
import protocol
#import noneprot								# noneprot
#import exprot									# exprot

port = 8081

server = protocol.Server(port)
#server = noneprot.Server(port)					# noneprot
#server = exprot.Server(port)					# exprot
server.main()

