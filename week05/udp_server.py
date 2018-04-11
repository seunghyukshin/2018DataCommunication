import socket 

ip_address = '127.0.0.1'
port_number = 3333
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number)) 
print("Server socket open....")
print("Listening...")

data_type,addr = server_sock.recvfrom(5000)
print("Received Message from client : "+data_type.decode())
data,addr = server_sock.recvfrom(5000)
print("Received Message from client : "+data.decode())

#print(data_type)
#print(data_type.decode())
if data_type.decode() == '0' :
#	print("wooooooow")
	data = data.upper()
#	print(data)
#	print(data.decode())
elif data_type.decode() == '1' :
	data = data.lower()
elif data_type.decode() == '2' :
	data = data.swapcase()
elif data_type.decode() == '3' :
#	data = ''.join(reversed(data))
	data = data[::-1]
print("Coverted msg : ",data.decode())

server_sock.sendto(data, addr)
print("Send to client converted msg..")

