# import socket
from socket import *

serverName = 'localhost'
serverPort = 55001
SERVER_ADDRESS = (serverName, serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)
sentence = input('Input lowercase sentence:')

clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(4096)
# print('From Server:', modifiedSentence.decode("UTF-8"))
print('From Server:', modifiedSentence.decode())

clientSocket.close()