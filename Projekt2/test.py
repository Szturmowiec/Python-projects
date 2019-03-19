#!/usr/bin/python
# -*- coding: utf-8 -*-
from socket import *
def main():
	# Create socket and bind to address
	UDPSock=socket(AF_INET,SOCK_DGRAM)
	UDPSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
	UDPSock.bind(("",2018))
	# Receive messages
	while True:
		data,addr=UDPSock.recvfrom(2018)
		if not data: break
		print(data,addr)
	# Close socket
	UDPSock.close()
main()