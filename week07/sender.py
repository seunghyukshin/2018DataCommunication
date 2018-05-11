import socket
import hashlib

receiverIP = '127.0.0.1'
receiverPort = 2345

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq_num = 0
h = hashlib.sha1()


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
while 1:
	if total_size - (1024*count) >= 1024:
		data = read_file.read(1024)
		checksum = str(seq_num).encode() + data
		h.update(checksum)
		data_packet = h.digest() + str(seq_num).encode() + data
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
		while 1 :
			if ACK.decode() == str((seq_num + 1) % 2) :
				break;
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		seq_num = (seq_num + 1) % 2
		count = count + 1
		print("(current size / total size) = " + str(1024*count) + "/" + str(total_size) + " , " + str(round(1024*count/total_size*100, 3)) + "%")
	else:
		remain_data_size = total_size - (1024*count)
		data = read_file.read(remain_data_size)
		checksum = str(seq_num).encode() + data
		h.update(checksum)
		data_packet = h.digest() + str(seq_num).encode() + data
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
		while 1 :
			if ACK.decode() == str((seq_num + 1) % 2) :
				break;
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		print("(current size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
		break
read_file.close()
