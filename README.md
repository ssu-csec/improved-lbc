# Improved LBC
   
A pure-Python implementation of LBC with supporting updates of ciphertext based on byte-level modifications of plaintext.
	   
## Installation
	    
Use ```git clone``` to install our project.
			     
```bash
git clone git@github.com:ssu-csec/improved-lbc.git
```
## Usage
					    
### Use Improved LBC(Mode of Operation of AES)
						   
If you just want to use ```Improbed LBC```, one of the modes of operation of AES, you can move the file ```crypto/aes.py``` and ```crypto/core.py``` to your project folder.
							  
Then, insert the code below at the first part of your code.
							     
```python
import aes
import core
```
For encrypting your data, you need the functions below:
									  
```python
encrypt(input string, enc_key, f_iv, b_iv)
gen_global(str_len)
global_enc(input_str, enc_key)
```
After encrypt your data and metadata, you can generate ```Data``` object with the output. It is the input type of ```decrypt``` function.
											 
For decrypting your ciphertext, you need the function below:
											  
```python
decrypt(input_data, dec_key)
```
The output of the function above is string type.

### Use Improved LBC Protocol
												    
If you need the protocol - safe server and clients - you can utilize ```crypto/protocol.py``` for your code.
```python
import core
import protocol
```
You can use ```Server``` and ```Client``` classes in ```protocol.py```.

```python
server = protocol.Server(port number, file name)
client - protocol.Client(socket, key, input queue)
```
```Server``` class has two inputs: port number and file name. 
When you execute a server with ```server.main()```, it opens the port specified by the input and waits clients to share contents of the file with the name provided as an input. 

After executing ```server.main()```, you can connect clients to the server by executing ```client.main(ip_address, port number)```. 
The input ```input queue``` of the constructor of ```Client``` functions as a channel through which the modifications made to the externally received data can be accessed and utilized within the functions of ```client``` object. 

You can push modification information to ```input_queue``` and the information should contain category of modification(Insert/Delete), the location of the modification(index) and the length(deletion) or inserted data(insertion).

## Test

For testing, we made ```test_s.py```(server) and ```test_c.py```(client).

The sequence for testing is as follows:

1. Create the file to be shared upon running the server program (it can be an empty file).
2. Run the server program and enter the port number and the name of the file to be shared(the file created in step 1).
3. Run the client program while providing the server's IP address and port number as inputs.
4. Upon running the client program, enter the data into the activated editor program.
5. Run additional instances of the client program to verify real-time sharing of the data.
