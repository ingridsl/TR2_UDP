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
clientSocket.settimeout(0.01) #0.001
base = 0
seq = 0
windowSize = 7
window = []
fim = False
#while(1):
#funcionamento
#message = raw_input('Input lowercase sentence:') 
f = open ("arq_teste.txt")
lastackrcv = time.time()

message = f.readline()
while not fim or window:
	if (seq < base + windowSize) and not fim:
		print message
		#newmes = ' '.join(format(ord(x), 'b') for x in message)
		#print "\nBinario da mensagem: " + newmes
		#val = 0
		#tam = len(newmes)
		#string = newmes
		#for x in range(0, tam):
		#	if(newmes[x] == '1') or (newmes[x] == '0'):
		#		val += ord(newmes[x])-48
		#print "Soma dos binarios: " + str(val)

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

		#envia/recebe dados
		#checksum = hashlib.md5()
		#md5 = checksum
		#checksum.update(message)
		#checksum.digest()
		#print len(str(checksum))
		print "Sequence number: " + str(seq)

		sndpkg = message + "*" + str(cs) + "*" + str(seq)
		window.append(sndpkg)

		#deixei comentado para tentar arrumar depois
		r = random.random()
		if (r <= 0.1): #simulacao de dado corrompido, probabilidade de 0.1
			print '\nSimulating bit error'
			error = random.getrandbits(8)
			listMsg = list(message)
			for i in range(5): #introduz 5 bits errados a mensagem
				randByte = random.randint(0, len(listMsg)-1)
				altByte = ord(listMsg[randByte]) & error
				listMsg[randByte] = struct.pack("B", altByte)
			message = "".join(listMsg)
			#print message
			sndpkg = message + "*" + str(cs) + "*" + str(seq)
		clientSocket.sendto(sndpkg,(serverName, serverPort)) 
		#clientSocket.sendto(md5,(serverName, serverPort))

		seq += 1
		if message == '':
			fim = True #esta aqui e nao depois da leitura, 
		#pq esta enviando um pacote extra vazio, para que identifique no servidor quando alcancou o fim do arquivo
		message = f.readline()

	try:
		ackMessage, serverAddress = clientSocket.recvfrom(2048)
		r = random.random()
		#print str(r)
		if (r <= 0.05): #simulacao de perda de pacote, probabilidade de 0.05
			print '\nSimulating acknowledgement loss\n'
			continue

		modifiedMessage, middle, received_cs = ackMessage.partition("*")
		received_cs, middle, exp_seq = received_cs.partition("*")
		print '\033[93m' + modifiedMessage + '\033[0m'

		#print "\nchecagem de erro : " + message
		#print str(ord(message[0]))
		#messagetst = raw_input()
		while int(exp_seq) > int(base) and window:
			#print '\nSEQ_RCV' + str(exp_seq) + ' > ' + str(base)
			lastackrcv = time.time()
			del window[0]
			base += 1

		if fim and (len(window) == 1):
			break;

	except:
		if (time.time()-lastackrcv > 0.1): #0.01
			print '\nERRO: ' + str(base)
			for i in window:
				#modifiedMessage, middle, received_bin = i.partition("*")
				#received_bin, middle, exp_seq = received_bin.partition("*")
				#print str(exp_seq)
				clientSocket.sendto(i,(serverName, serverPort)) 

#fechar socket
f.close()
clientSocket.close()
print '\nConnection closed'