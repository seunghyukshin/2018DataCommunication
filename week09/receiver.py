import socket
import hashlib
import struct

ip_address = '127.0.0.1'
port_number = 2345

seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
seqIndex = 0

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

info_packet,addr = server_sock.recvfrom(1045)
info_checksum = info_packet[:20]
info_seqAndACK = info_packet[20:21]
file_info = info_packet[21:]

h = hashlib.sha1()
h.update(info_seqAndACK + file_info)


seqNum = seqList[seqIndex] << 4
ACK = seqList[seqIndex]
seqIndex = (seqIndex + 1) % 8
seqAndACK = (seqNum|ACK).to_bytes(1, "big")

# send seqAndACK.
server_sock.sendto(seqAndACK, addr)

print("Send file info ACK...")
total_size = struct.unpack("!i", file_info[:4])[0]
file_name = file_info[4:].decode()
path = "./newDir/"+file_name
print("file Name = " + file_name)
print("file Size = " + str(total_size))
print("received file Path = " + path)

#reopen
write_file = open(path, "wb")

count = 0
current_size = 0
while current_size != total_size:
	h = hashlib.sha1()
	data_packet,addr = server_sock.recvfrom(1045)
	data_checksum = data_packet[:20]
	data_seq_num = data_packet[20:21]
	data_info = data_packet[21:]
	h.update(data_seq_num + data_info)
	

	if data_checksum == h.digest():
		count += 1
		current_size += len(data_info)
		write_file.write(data_info)

		seqNum = seqList[seqIndex] << 4
		ACK = seqList[seqIndex]
		seqIndex = (seqIndex + 1) % 8
		seqAndACK = (seqNum|ACK).to_bytes(1, "big")

		server_sock.sendto(seqAndACK, addr)
		
		print("(current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
	
write_file.close()
