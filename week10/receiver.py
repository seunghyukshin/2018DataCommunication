import socket
import hashlib
import struct
import time
 
ip_address = '127.0.0.1'
port_number = 2345
 
seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
seqIndex = 0
 
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")
 
infoPacket,addr = server_sock.recvfrom(1045)
infoChecksum = infoPacket[:20]
infoSeqAndACK = infoPacket[20:21]
fileInfo = infoPacket[21:]
 
h = hashlib.sha1() 
h.update(infoSeqAndACK + fileInfo)
 
seqNum = seqList[seqIndex] << 4
ACK = seqList[seqIndex]
seqIndex = (seqIndex + 1) % 8
seqAndACK = (seqNum|ACK).to_bytes(1, "big")

# send seqAndACK. 
server_sock.sendto(seqAndACK, addr)
 
print("Send file info ACK...")
total_size = struct.unpack("!i", fileInfo[:4])[0]
file_name = fileInfo[4:].decode()
path = "./new_dir/"+file_name
print("file Name = " + file_name)
print("file Size = " + str(total_size))
print("received file Path = " + path)
 
#reopen
write_file = open(path, "wb")
 
count = 0
current_size = 0
check = 1
while current_size != total_size:
	h = hashlib.sha1()
	data_packet,addr = server_sock.recvfrom(1045)
	data_checksum = data_packet[:20]
	data_seq_num = data_packet[20:21]
	data_info = data_packet[21:]
	h.update(data_seq_num + data_info)
 	
	recv_seq = data_seq_num.hex()[0:1]

	if count == 15:
		print("Wait for 5...")
		count += 1
		time.sleep(5)

	elif data_checksum == h.digest():
		checkSeqNum = seqList[check]<<4
		checkACK = seqList[check]
		checkSeqAndACK = (checkSeqNum|checkACK).to_bytes(1, "big")
		
		if data_seq_num == checkSeqAndACK: 
			count += 1
			check = (check + 1) % 8
			current_size += len(data_info)
			write_file.write(data_info)

			seqNum = seqList[seqIndex] << 4
			ACK = seqList[seqIndex]
			seqIndex = (seqIndex + 1) % 8
			seqAndACK = (seqNum|ACK).to_bytes(1, "big")
			
			server_sock.sendto(seqAndACK, addr)

			print("(current size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
		else:
			index = check
			print("Discard Packet: SEQ=" + str(recv_seq) + " ACK=" + str(recv_seq))
	else:
		# if NAK	
		seqNum = seqList[seqIndex] << 4
		NAK = 0b1111
		seqAndNAK = (seqNum|NAK).to_bytes(1, "big")
		server_sock.sendto(seqAndACK, addr)
		print("*** Send NAK!! ***")

write_file.close()


 
