import socket
import hashlib

receiverIP = '127.0.0.1'
receiverPort = 2345

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_sock.settimeout(3)
seq_num = 0
#h = hashlib.sha1()
NAK = 2

print("Sender Socket open...")
print("Receiver IP = " + receiverIP)
print("Receiver Port = " + str(receiverPort))
print("Send File Info to Server...")
file_name = "image.png"
read_file = open("./"+file_name, "rb")
total_size = len(read_file.read())

#file info sending 
file_info = total_size.to_bytes(4, byteorder = "big") + file_name.encode()
sender_sock.sendto(file_info, (receiverIP, receiverPort))
ACK = sender_sock.recv(1)
print("Start File send")
seq_num = (seq_num + 1) % 2
read_file.close()

#reopen
read_file = open("./"+file_name, "rb")
#DATA SENDING
count = 0
current_size=0
while 1:
	if current_size >= total_size :
		break;	
	try:

		count = count + 1
		h=hashlib.sha1()
		data = read_file.read(1024)
		checksum = str(seq_num).encode() + data
		#if count == 15: ## wrong checksum
		#	checksum = data
		h.update(checksum)
		data_packet = h.digest() + str(seq_num).encode() + data
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
		while 1 :
			#print(ACK.decode())
			#print(str(NAK))
			if ACK.decode() != str(NAK) :
				break
			print(" * Received NAK - Retransmit!")
			print("Retransmission : (current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
				
			h=hashlib.sha1()
			checksum = str(seq_num).encode() + data
			h.update(checksum)
			data_packet = h.digest() + str(seq_num).encode() + data	
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
			
		current_size += len(data)
		print("(current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3)) + "%")
	
	except socket.timeout as e:
		current_size += len(data)
		print(" * Time Out!! ***")
		print("Retransmission : (current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))


read_file.close()
