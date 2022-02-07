# import socket
from socket import *
from User import *
'''
    Left to Do:
        - need to find a way to start connection (done for basic use)
        - select who to send to
        - 
    How it works so far:
        - when a client connects to the server he sends his name first that 
          gets appended to the connections dictionary including his connection socket.
'''
SERVER_ADDRESS = ('', 55002)
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
        print(user.username)
    # Find to whom the message is for and send
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
