from socket import *
from decimal import *
import pickle
import hashlib
import sys
import os
import math
import time
import random
import struct
serverName = '' 	#IP do servidor
serverPort = 12000 	# porta do servidor

# criando socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(0.001)
base = 0
seq = 0
windowSize = 7
window = []
fim = False
f = open ("arq_teste.txt")
lastackrcv = time.time()
lastpkgsnd = 0 ###

message = f.readline()
while not fim or window:
	if (time.time()-lastpkgsnd > 0.001): ###
		if (seq < base + windowSize) and not fim:
			print "\nSEND" ###
			print message

			auxMsg = message
			sum = 0
			if (len(auxMsg) % 2) != 0:
				auxMsg += "0"
			for i in range(0, len(auxMsg), 2):
				msg16 = ord(auxMsg[i]) + (ord(auxMsg[i+1]) << 8)
				sum += msg16
				sum = (sum & 0xffff) + (sum >> 16)
			cs = ~sum & 0xffff
			print "Checksum: " + str(cs)

			print "Sequence number: " + str(seq)

			sndpkg = message + "*" + str(cs) + "*" + str(seq)
			window.append(sndpkg)

			r = random.random()
			if (message != '') and (r <= 0.1): #simulacao de dado corrompido, probabilidade de 0.1
				print '\033[91m' + '\nSimulating bit error' + '\033[0m'
				error = random.getrandbits(8)
				listMsg = list(message)
				for i in range(5): #introduz 5 bits errados a mensagem
					randByte = random.randint(0, len(listMsg)-1)
					altByte = ord(listMsg[randByte]) & error
					listMsg[randByte] = struct.pack("B", altByte)
				message = "".join(listMsg)
				sndpkg = message + "*" + str(cs) + "*" + str(seq)
			clientSocket.sendto(sndpkg,(serverName, serverPort)) 
			lastpkgsnd = time.time() ###

			seq += 1
			if message == '':
				fim = True 
			message = f.readline()
		else:
			if not(seq < base + windowSize):
				print "buffer cheio..."

	try:
		ackMessage, serverAddress = clientSocket.recvfrom(2048)
		#r = random.random()
		#if not fim and (r <= 0.05): #simulacao de perda de pacote, probabilidade de 0.05
		#	print  '\033[91m'+'\nSimulating acknowledgement loss\n'+'\033[0m'
		#	continue

		modifiedMessage, middle, received_cs = ackMessage.partition("*")
		received_cs, middle, exp_seq = received_cs.partition("*")
		print '\033[93m' + modifiedMessage + '\033[0m'

		while int(exp_seq) > int(base) and window:
			lastackrcv = time.time()
			del window[0]
			base += 1
			print "movimentando janela... base = " + str(base)

		if fim and (len(window) == 1):
			break;

	except:
		print "\nEXCEPT: " + str(time.time()) + " - " + str(lastackrcv) + " = " + str(time.time()-lastackrcv) ###
		if (time.time()-lastackrcv > 0.002): #0.01 ###
			print '\nERRO: ' + str(base) + "->" + str(seq) ###
			for i in window:
				clientSocket.sendto(i,(serverName, serverPort)) 

#fechar socket
f.close()
clientSocket.close()
print '\nConnection closed'
