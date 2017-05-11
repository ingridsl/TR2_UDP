from socket import *
serverName = '' 	#IP do servidor?
serverPort = 12000 	# porta do servidor

# criando socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

#funcionamento?
message = raw_input('Input lowercase sentence:') 

#envia/recebe dados
clientSocket.sendto(message,(serverName, serverPort)) 
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
print modifiedMessage

#fechar socket
clientSocket.close()