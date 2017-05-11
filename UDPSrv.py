from socket import *
import pickle
import hashlib
import sys
import os
import math
import time
serverPort = 12000	# porta do servidor

#criar socket e coloca endereco de ip no socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


#inicializa variaveis
seqNum = 1
ACK = 1
ack = []

print 'The server is ready to receive'
#envia/recebe dados
while 1:
	rcvpkt=[]
	message, clientAddress = serverSocket.recvfrom(2048)
	rcvpkt = pickle.loads(message) #dando erro aqui
	print rcvpkt
	print message
#		check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT
	c = rcvpkt[-1]
	del rcvpkt[-1]
	h = hashlib.md5()
	print h
	print c
	h.update(pickle.dumps(message))
	print h.digest()
	print 'the end'
	if message == h.digest():
		print 'oi'
	else:
		print "error detected"
	#print checksum
	#if(checksum == 1 and message[48:64] == '01' * 8):
	#	print "New Ack"
	#else:
	#	print "Packet Discarded, Checksum not matching!!!"


	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
