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
print "\nbinario da mensagem: " + newmes

val = 0
tam = len(newmes)

string = newmes
for x in range(0, tam):
		if(newmes[x]=='1')or (newmes[x] =='0'):
			val+= ord(newmes[x])-48

print "\nsoma dos binarios: " + str(val)
#envia/recebe dados
#checksum = hashlib.md5()
#md5 = checksum
#checksum.update (message)
#checksum.digest()
#print len(str(checksum))
#print str(checksum)

clientSocket.sendto(message + " " + str(val),(serverName, serverPort)) 
#clientSocket.sendto(md5,(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
print modifiedMessage

#fechar socket
clientSocket.close()