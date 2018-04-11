import socket
import struct

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

while True:
	packet = sock.recvfrom(4096)
	

	print("----------------------------------")
	print("------------Ethernet--------------")
	print("----------------------------------")
	ethernet_header = struct.unpack('!6s6s2s',packet[0][0:14])
	dst_ea = ethernet_header[0].hex()
	dst_ethernet_addr =""+str(dst_ea[0:2])+":"+str(dst_ea[2:4])+":"+str(dst_ea[4:6])+":"+str(dst_ea[6:8])+":"+str(dst_ea[8:10])+":"+str(dst_ea[10:12])
	src_ea = ethernet_header[1].hex()
	src_ethernet_addr =""+str(src_ea[0:2])+":"+str(src_ea[2:4])+":"+str(src_ea[4:6])+":"+str(src_ea[6:8])+":"+str(src_ea[8:10])+":"+str(src_ea[10:12])
	protocol_type = "0x"+ethernet_header[2].hex()

	print("destination : ",dst_ethernet_addr)
	print("source : ",src_ethernet_addr)
	print("protocol : ",protocol_type)
	
	if not protocol_type == ('0x0800') :
		break

	print("----------------------------------")
	print("--------------IPv4----------------")
	print("----------------------------------")
	ipv4_header = struct.unpack('!BBHHHBBH4s4s',packet[0][14:34])
	ver_ipv4 = ipv4_header[0] >> 4
	header_length_ipv4 = (ipv4_header[0]&0x0f) << 2
#	header_length_ipv4 = ipv4_header[0]
	service_ipv4 = ipv4_header[1]
	total_length_ipv4 = ipv4_header[2]
	identifier_ipv4 = ipv4_header[3]
	flags_ipv4 = ipv4_header[4]>>13
	frag_offset_ipv4 = (ipv4_header[4]&0x1fff)
	ttl_ipv4 = ipv4_header[5]
	protocol_ipv4 = ipv4_header[6]
	checksum_ipv4 = ipv4_header[7]
	src = ipv4_header[8].hex()
	src_ipv4_addr =""+str(int(src[0:2], 16))+"."+str(int(src[2:4], 16))+"."+str(int(src[4:6], 16))+"."+str(int(src[6:8], 16))
	dst = ipv4_header[9].hex()
	dst_ipv4_addr =""+str(int(dst[0:2], 16))+"."+str(int(src[2:4], 16
))+"."+str(int(src[4:6], 16))+"."+str(int(src[6:8], 16))
	print("version : ",ver_ipv4)
	print("header length : ",header_length_ipv4)
	print("type of service or DiffServ : ",service_ipv4)
	print("total length : ",total_length_ipv4)
	print("Identifier : ",identifier_ipv4)
	print("Flags : ",flags_ipv4)
	print("Fragment Offset : ",frag_offset_ipv4)
	print("Time to Live : ",ttl_ipv4)
	print("Protocol : ",protocol_ipv4)
	print("Header Chechsum : ",checksum_ipv4)
	print("Source Address : ",src_ipv4_addr) 
	print("Destination Address : ",dst_ipv4_addr)

        #IPV의 Headerlength를 확인해서 UDP와 TCP 몇바이트 파싱할 건지에 대한 구현 
	start_index = header_length_ipv4 + 14
	if protocol_ipv4 == 6 :	#20B
		print("----------------------------------")
		print("---------------TCP----------------")
		print("----------------------------------")
		
		tcp_header = struct.unpack('!HHIIBBHHH',packet[0][start_index:54])
		src_tcp = tcp_header[0]
		dst_tcp = tcp_header[1]
		seq_num_tcp = tcp_header[2]
		ack_num_tcp = tcp_header[3]
		offset_tcp = (tcp_header[4]&240)>>4
		reserved_tcp = (tcp_header[4]&14)>>1
		ns = tcp_header[4] & 1
		flag = tcp_header[5]
		cwr = flag >> 7
		ece = (flag & 64) >> 6 
		urg = (flag & 32) >> 5 
		ack = (flag & 16) >> 4
		psh = (flag & 8) >> 3
		rst = (flag & 4) >> 2
		syn = (flag & 2) >> 1
		fin = flag & 1		
		win_size_tcp = tcp_header[6]
		checksum_tcp = tcp_header[7]
		urg_pointer_tcp = tcp_header[8]
		
		print("Source Port : ",src_tcp)
		print("Destination Port : ",dst_tcp)
		print("Sequence Number : ",seq_num_tcp)
		print("Acknoledge Number : ",ack_num_tcp)
		print("Data offset : ",offset_tcp)
		print("Reserved : ",reserved_tcp)
		print("NS : ",ns)
		print("CWR : ",cwr)
		print("ECE : ",ece)
		print("URG : ",urg)
		print("ACK : ",ack)
		print("PSH : ",psh)	
		print("RST : ",rst)
		print("SYN : ",syn)
		print("FIN : ",fin)
		print("Window Size : ",win_size_tcp)
		print("TCP checksum : ",checksum_tcp)
		print("Urgent Pointer : ",urg_pointer_tcp)


	if protocol_ipv4 == 17 : #8B
		print("----------------------------------")
		print("---------------UDP----------------")
		print("----------------------------------")
		
		udp_header = struct.unpack('!HHHH',packet[0][start_index:42])
		src_udp = udp_header[0];
		dst_udp = udp_header[1];
		length_udp = udp_header[2];
		checksum_udp = udp_header[3];
		
		print("Source Port : ",src_udp)
		print("Destination Port : ",dst_udp)
		print("UDP Length : ",length_udp)
		print("UDP Checksum : ",checksum_udp)

	#udp_header = struct.unpack('!6s6s2s',packet[0][0:14])
	




	
