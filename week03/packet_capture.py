import socket
import struct

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

while True:
	packet = sock.recvfrom(4096)
	
	ethernet_header = struct.unpack('!6s6s2s',packet[0][0:14])
	dst_ea = ethernet_header[0].hex()
	dst_ethernet_addr =""+str(dst_ea[0:2])+":"+str(dst_ea[2:4])+":"+str(dst_ea[4:6])+":"+str(dst_ea[6:8])+":"+str(dst_ea[8:10])+":"+str(dst_ea[10:12])
	src_ea = ethernet_header[1].hex()
	src_ethernet_addr =""+str(src_ea[0:2])+":"+str(src_ea[2:4])+":"+str(src_ea[4:6])+":"+str(src_ea[6:8])+":"+str(src_ea[8:10])+":"+str(src_ea[10:12])
	protocol_type = "0x"+ethernet_header[2].hex()

	print("destination : ",dst_ethernet_addr)
	print("source : ",src_ethernet_addr)
	print("protocol : ",protocol_type)
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
        
	break
