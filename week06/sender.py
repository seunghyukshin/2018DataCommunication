import socket

serverIP = '127.0.0.1'
serverPort = 2345

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((serverIP, serverPort))
print("Connect to Server...")
print("Receiver IP = " + str(serverIP))
print("Receiver Port = "+ str(serverPort))
fileName = input("Input File Name : ")

readFile = open("./"+fileName,"rb")
  
data = readFile.read() 
print("File Size =" +str(len(data)))
readFile = open("./"+fileName,"rb")

gap = 11 - len(fileName)

if gap is not 0:
	fileName = " "*gap +fileName

packetTypeMsg = "0"
packetTypeData = "1"
currentSize = 0
totalSize = len(data)

encodeFileSize = len(data).to_bytes(4, byteorder = "big")
packetHeader = packetTypeMsg.encode() + fileName.encode() + encodeFileSize
client_sock.send(packetHeader)

#send file
if totalSize < 1024:
	packetData = packetHeader + readFile.read(totalSize)
	client_sock.send(packetData)
	print("(current size / total size) = " + str(totalSize) + "/" + str(totalSize) + " , 100.0%")
else :
	count =0;
	while totalSize-(1024*count) >= 1024:
		packetData = packetHeader + readFile.read(1024)
		client_sock.send(packetData)
		count = count + 1
		print("(current size / total size) = " + str(1024*count) + "/" + str(totalSize) + " , " + str(round(1024*count/totalSize*100, 3)) + "%")
	remainDataSize = totalSize - (1024*count)
	packetData = packetHeader + readFile.read(remainDataSize)
	client_sock.send(packetData)
	print("(current size / total size) = " + str(totalSize) + "/" + str(totalSize) + " , 100.0%")
print("File send end.")

#client_msg = input("Input your MSG: ")
#client_sock.send(client_msg.encode())
#print("Send Message to Server ... ")
#print("Received msg from Server : "+(client_sock.recv(1024)).decode('utf-8'))
#print("File send end")
readFile.close()
