import socket

serverIP = '127.0.0.1'
serverPort = 3333

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=================================")
print("======String Change Program======")
print("=================================")
print("type = 0,1,2,3")
print("if 0 : change all letters to uppercase")
print("if 1 : change all letters to lowercase")
print("if 2 : 대문자는소문자 소문자는대문자로")
print("if 3 : 뒤집기")

client_type = input("Input Type : ")
client_sock.sendto(client_type.encode(), (serverIP, serverPort))
client_msg = input("Input your Message : ")
client_sock.sendto(client_msg.encode(), (serverIP, serverPort))
print("Send Message to Server..")

print("Received Message from Server :"+(client_sock.recv(1024)).decode())
