import socket
import struct

ip_address = '127.0.0.1'
port_number = 2345
path="./receivedFolder/"

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening....")
server_sock.listen()

client_sock,addr = server_sock.accept()
print("Connected with client")

data = client_sock.recv(16)
currentSize =0 
totalSize = struct.unpack("!i",data[12:16])[0]

print("Packet Type = "+ data[0:1].decode())
print("File Size = "+str(totalSize))

fileName = ""
for i in data[1:12].decode():
	if i is not " ":
		fileName += i
path += fileName
print("File Path = "+path)

writeFile = open(path,"wb")

#receive data
if totalSize<1024:
	receiveData = client_sock.recv(16+totalSize)
	writeFile.write(receiveData[16:])
	print("(current size / total size) = " + str(totalSize) + "/" + str(totalSize) + " , 100.0%")

else:
	count = 0
	while totalSize - (1024*count) >= 1024:
		receiveData = client_sock.recv(1040)
		writeFile.write(receiveData[16:])
		count = count + 1
		print("(current size / total size) = " + str(1024*count) + "/" + str(totalSize) + " , " + str(round(1024*count/totalSize*100, 3)) + "%")
	remainDataSize = totalSize - (1024*count)
	receiveData = client_sock.recv(16 + remainDataSize)
	writeFile.write(receiveData[16:])
	print("(current size / total size) = " + str(totalSize) + "/" + str(totalSize) + " , 100.0%")


#print("Received Message from client : "+data.decode())

#client_sock.send(data)
#print("Send Message back to client")
#print("File receive end.")
writeFile.close()


