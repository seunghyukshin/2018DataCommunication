import socket
import hashlib
import struct
import time

ip_address = '127.0.0.1'
port_number = 2345


h = hashlib.sha1()
seq_num = 0
NAK = 2

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...") 

#file info Receive
file_info,addr = server_sock.recvfrom(1045)
seq_num = (seq_num + 1) % 2

#ACK Send
server_sock.sendto(str(seq_num).encode(), addr)
print("Send file info ACK...")

#if time over/ 
#file info unpack&decode
total_size = struct.unpack("!i", file_info[:4])[0]
file_name = file_info[4:].decode()
path = "./newDirectory/"+file_name
print("file Name = " + file_name)
print("file Size = " + str(total_size))
print("received file Path = " + path)


write_file = open(path, "wb")
#DATA RECEIVING
count = 0
current_size = 0
while 1:
	if current_size >= total_size :
		break;
	h = hashlib.sha1()
	data_packet,addr = server_sock.recvfrom(1045)
	data_checksum = data_packet[:20]
	data_seq_num = data_packet[20:21]
	data_info = data_packet[21:]
	h.update(data_seq_num + data_info)

	while data_checksum != h.digest():
		print(" * Packet corrupted!! *** - Send To Sender NAK(2)")
		h = hashlib.sha1()
		server_sock.sendto(str(NAK).encode(), addr)
		data_packet,addr = server_sock.recvfrom(1045)
		data_checksum = data_packet[:20]
		data_seq_num = data_packet[20:21]
		data_info = data_packet[21:]
		h.update(data_seq_num + data_info)

	if count == 10:
		print("Wait for 5...")
		count += 1
		time.sleep(5)
	else:	
		count += 1
		current_size += len(data_info)
		write_file.write(data_info)


		seq_num = (seq_num + 1) % 2
		server_sock.sendto(str(seq_num).encode(), addr)

	
		print("(current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3)) + "%")
	

write_file.close()
