# import socket
from socket import *
import concurrent.futures
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
SERVER_ADDRESS = ('', 55016)
serverSocket = socket(AF_INET, SOCK_STREAM)
connections = {}
sock ={}
serverSocket.bind(SERVER_ADDRESS)
serverSocket.listen(5)
print("The server is ready to receive clients")

def run():
    connection_socket, addr_client = serverSocket.accept()
    while True:
        if addr_client not in connections.keys():
            print(addr_client)
            user = User()
            user.set_user(connection_socket.recv(4096).decode(), addr_client)
            connections[addr_client] = user
            sock[user] = connection_socket
            user.connected_user = connection_socket
            print(user.username)
        # Find to whom the message is for and send
        sentence = connection_socket.recv(4096).decode()
        print('the sentence is ' + sentence)
        if sentence == '<get_users>':
            connection_socket.send(bytes(str(connections).encode()))

        elif sentence[:9] == '<connect_' and sentence[len(sentence)-1:len(sentence)] == '>':
            for connection in connections.values():
                print(connection)
                print(sentence[len(sentence) - 1:len(sentence)])
                print(sentence[9:len(sentence)])
                if connection.username == sentence[9:len(sentence)-1]:
                    connections[addr_client].connected_user = sock[connection]
                    connection.connected_user = connection_socket
            connection_socket.send(bytes('connected!'.encode()))
        else:
            sentencefrom = connections[addr_client].username + ': '
            print(sentencefrom + sentence)
            connection_socket.send(bytes('Sent!\n'.encode()))
            connections[addr_client].connected_user.send(bytes(sentencefrom.encode() + sentence.encode()))



# ThreadPool run 5 threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    clients = [executor.submit(run) for _ in range(5)]
