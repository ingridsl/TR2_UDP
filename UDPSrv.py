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
	received_hash=[]
	received_message = []
	full_info, clientAddress, = serverSocket.recvfrom(2048)
	
	print full_info
	received_hash = full_info[0:34]
	message = full_info[34:]
	message+"\0"

	print "\nreceived_hash: " + received_hash
	print "\nreceived_message: " + message

#		check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT
	#c = rcvpkt[-1]
	#del rcvpkt[-1]
	calculated_hash = hashlib.md5(message)
	#print c
	calculated_hash.update(message)
	calculated_hash.digest()
	print "\ncalculated_hash.digest(): " + str(calculated_hash)
	print '\nthe end: '
	if received_hash == calculated_hash:
		print '\nAEEEEEEEE'
	else:
		print "\nerror detected"
	#print checksum
	#if(checksum == 1 and message[48:64] == '01' * 8):
	#	print "New Ack"
	#else:
	#	print "Packet Discarded, Checksum not matching!!!"


	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
