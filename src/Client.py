# import socket
from socket import *
def init_connect(clientSocket,username):
    clientSocket.send(username.encode())
serverName = 'localhost'
serverPort = 55002
SERVER_ADDRESS = (serverName, serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)

username = input('Input Username:')
init_connect(clientSocket,username)
message = input('send message:')
#modifiedSentence = clientSocket.recv(4096)
clientSocket.send(message.encode())
# print('From Server:', modifiedSentence.decode("UTF-8"))
modifiedSentence = clientSocket.recv(4096)
print('From Server:', modifiedSentence.decode())

clientSocket.close()