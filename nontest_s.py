import core
import protocol
import noneprot

port = int(input("Input port number: "))
size = input("Choose size of the data: ")

f_name = "none_server_" + size + ".txt"

server = noneprot.Server(port, f_name)	

server.main()


