from socket import *
import pickle
import hashlib
import sys
import os
import math
import time
import random
serverPort = 12000	# porta do servidor

#criar socket e coloca endereco de ip no socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(5)

#inicializa variaveis
ACK = 1
ack = []
seq_exp = 0
print 'The server is ready to receive'
lastpkgrcv = time.time()	
starttime = time.time()
endoffile = False

#envia/recebe dados
while 1:
	try:
		received_bin = []
		received_message = []
		full_info, clientAddress = serverSocket.recvfrom(2048)
		
		#print full_info
		#name = full_info
		#received_hash = full_info[0:34]
		#message = full_info[34:]
		#message+"\0"
		message, middle, received_cs = full_info.partition("*")
		#print message + "\n" + received_bin

		received_cs, middle, sequence_number = received_cs.partition("*")
		#print received_bin + "\n" + sequence_number

		#print "\nreceived_bin: " + received_bin
		#print "\nreceived_message: " + message

		#	check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT

		#newmes = ' '.join(format(ord(x), 'b') for x in message)
		#print "\nbinario da mensagem: " + newmes

		#calculated_bin = 0
		#tam = len(newmes)

		#string = newmes
		#for x in range(0, tam):
		#	if(newmes[x] == '1') or (newmes[x] == '0'):
		#		calculated_bin += ord(newmes[x])-48

		auxMsg = message
		sum = 0
		if (len(auxMsg) % 2) != 0:
			auxMsg += "0"
		for i in range(0, len(auxMsg), 2):
			msg16 = ord(auxMsg[i]) + (ord(auxMsg[i+1]) << 8)
			sum += msg16
			sum = (sum & 0xffff) + (sum >> 16)
		calculated_cs = ~sum & 0xffff

		#print "\nreceived_bin: " + received_bin
		#print "\nsoma dos binarios calculada: " + str(calculated_bin)
		print "\nChecksum calculado: " + str(calculated_cs)
		print "Sequence number: " + str(seq_exp)

		#	check value of expected seq number against seq number received - IN ORDER 
		if str(received_cs) == str(calculated_cs): # recebido sem estar corrompido
			if(str(sequence_number) == str(seq_exp)): #na ordem
				r = random.random()
				if (r <= 0.1): #simulacao de perda de pacote, probabilidade de 0.1
					print '\nSimulating packet loss'
					continue
				if (message == ''):
					endoffile = True
				modifiedMessage = message.upper()
				ackmsg = modifiedMessage + "*" + str(calculated_cs) + "*" + str(seq_exp)
				serverSocket.sendto(ackmsg, clientAddress)
				seq_exp += 1
			else: #fora da ordem
				print '\nerror detected - OUT OF ORDER'
				modifiedMessage = message.upper()
				ackmsg = modifiedMessage + "*" + str(calculated_cs) + "*" + str(seq_exp)
				serverSocket.sendto(ackmsg, clientAddress)
		else:
			print "\nerror detected - CORRUPTION"
	
	except:
		if endoffile:
			if(time.time()-lastpkgrcv > 5):
				break
		
endtime = time.time()

print '\nFILE TRANFER SUCCESSFUL'
print "TIME TAKEN " , str(endtime - starttime)