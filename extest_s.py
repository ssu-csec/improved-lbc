import core
import protocol
import exprot					

port = int(input("Input port number: "))
size = input("Choose size of the data: ")
mode = input("Choose mode CTR or CBC: ")
f_name = "ex_server_" + size + "_" + mode + ".p"

server = exprot.Server(port, f_name)	

server.main()


