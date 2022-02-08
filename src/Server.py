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
SERVER_ADDRESS = ('', 55000)
serverSocket = socket(AF_INET, SOCK_STREAM)
connections = {}
addresses = {}
serverSocket.bind(SERVER_ADDRESS)
serverSocket.listen(5)
print("The server is ready to receive clients")

while True:
    connectionSocket, addrClient = serverSocket.accept()
    print('got somthing!')
    # First connection.
    if addrClient[0] not in connections.keys():
        print(addrClient)
        user = User()
        user.set_user(connectionSocket.recv(4096).decode(), addrClient)
        connections[addrClient[0]] = user
        addresses[user]=addrClient
        print(user.username)
    # Find to whom the message is for and send
    connectionSocket.settimeout(1)
    sentence = connectionSocket.recv(4096).decode()
    print(sentence)
    connected_user = connections[addrClient[0]].connected_user
    sentencefrom = connected_user.username+':'
    print(sentencefrom+sentence)
    connectionSocket.sendto(bytes(sentencefrom.encode()), addresses[connected_user])
    connectionSocket.sendto(bytes(sentence.encode()),addresses[connected_user])
    connectionSocket.close()
