from socket import *
from decimal import *
import pickle
import hashlib
import sys
import os
import math
import time
serverName = '' 	#IP do servidor?
serverPort = 12000 	# porta do servidor

# criando socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

#funcionamento?
message = raw_input('Input lowercase sentence:') 
newmes = ' '.join(format(ord(x), 'b') for x in message)
print newmes

val=0
print newmes[3]

tam = len(newmes)
arre = range(0, tam)
print tam
arre2 = list(range(0, tam))

for i in range(0, tam)
	#if(newmes[i]=='1' ||newmes[i] =='0)
	#	val+= newmes[x]

print val
#envia/recebe dados
checksum = hashlib.md5()
md5 = checksum
print len(str(checksum))
checksum.update (message)
checksum.digest()
print len(str(checksum))
print str(checksum)

clientSocket.sendto(str(str(checksum)+message),(serverName, serverPort)) 
#clientSocket.sendto(md5,(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
print modifiedMessage

#fechar socket
clientSocket.close()