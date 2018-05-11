import socket
import hashlib
import struct

ip_address = '127.0.0.1'
port_number = 2345


h = hashlib.sha1()
seq_num = 0


server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

file_info,addr = server_sock.recvfrom(1045)
seq_num = (seq_num + 1) % 2
server_sock.sendto(str(seq_num).encode(), addr)
print("Send file info ACK...")
total_size = struct.unpack("!i", file_info[:4])[0]
file_name = file_info[4:].decode()
path = "./newDirectory/"+file_name
print("file Name = " + file_name)
print("file Size = " + str(total_size))
print("received file Path = " + path)


write_file = open(path, "wb")
#DATA RECEIVING
count = 0
while 1:
	data_packet,addr = server_sock.recvfrom(1045)
	data_checksum = data_packet[:20]
	data_seq_num = data_packet[20:21]
	data_info = data_packet[21:]
	h.update(data_seq_num + data_info)

	while data_checksum != h.digest():
		server_sock.sendto(str(seq_num).encode(), addr)
		data_packet,addr = server_sock.recvfrom(1045)
		data_checksum = data_packet[:20]
		data_seq_num = data_packet[20:21]
		data_info = data_packet[21:]
		h.update(data_seq_num + data_info)

	seq_num = (seq_num + 1) % 2
	server_sock.sendto(str(seq_num).encode(), addr)

	if total_size - (1024*count) >= 1024:
		write_file.write(data_info)
		count = count + 1
		print("(current size / total size) = " + str(1024*count) + "/" + str(total_size) + " , " + str(round(1024*count/total_size*100, 3)) + "%")
	else:
		write_file.write(data_info)
		print("(current size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
		break

write_file.close()
