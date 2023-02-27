import core
import protocol

port = int(input("Input port number: "))
size = input("Choose size of the data: ")
f_name = "test_server_" + size + ".p"
server = protocol.Server(port, f_name)
server.main()


