# import socket
from socket import *
from User import *

SERVER_ADDRESS = ('', 55001)
serverSocket = socket(AF_INET, SOCK_STREAM)
connections = {}
addresses = []
serverSocket.bind(SERVER_ADDRESS)
serverSocket.listen(5)
print("The server is ready to receive clients")
while True:
    connectionSocket, addrClient = serverSocket.accept()
    # First connection.
    if addrClient not in addresses:
        addresses.append(addrClient)
        user = User()
        user.set_user(connectionSocket.recv(4096).decode(), addrClient)
        connections[connectionSocket] = user
    # Find to who the message is for and send
    else:
        sentence = connectionSocket.recv(4096).decode()
        connected_user = connections[connectionSocket].connected_user
        keys = connections.keys()
        sendsock = None
        for key in keys:
            if connections[key] == connected_user:
                sendsock = key
        if sendsock is None:
            print("No such user")
        print("Get from client ", addrClient, ":", sentence)
        sendsock.send(bytes(sentence.encode()))
        # connectionSocket.send(capitalizedSentence).encode()
        connectionSocket.close()
