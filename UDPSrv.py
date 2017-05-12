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
	received_bin=[]
	received_message = []
	full_info, clientAddress, = serverSocket.recvfrom(2048)
	
	print full_info
	name = full_info
	#received_hash = full_info[0:34]
	#message = full_info[34:]
	#message+"\0"
	message, middle, received_bin = name.partition(" ")
	print message + "\n" + received_bin





	print "\nreceived_bin: " + received_bin
	print "\nreceived_message: " + message

#		check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT

	newmes = ' '.join(format(ord(x), 'b') for x in message)
	print "\nbinario da mensagem: " + newmes

	calculated_bin = 0
	tam = len(newmes)

	string = newmes
	for x in range(0, tam):
			if(newmes[x]=='1')or (newmes[x] =='0'):
				calculated_bin+= ord(newmes[x])-48


	print "\nsoma dos binarios: " + str(calculated_bin)

	#		check value of expected seq number against seq number received - IN ORDER 
	if str(received_bin) == str(calculated_bin):
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
