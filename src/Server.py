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
SERVER_ADDRESS = ('', 55008)
serverSocket = socket(AF_INET, SOCK_STREAM)
connections = {}
addresses = {}
sock ={}
serverSocket.bind(SERVER_ADDRESS)
serverSocket.listen(5)
print("The server is ready to receive clients")


def run():
    connection_socket, addr_client = serverSocket.accept()
    newsock = connection_socket
    while True:
        if addr_client not in connections.keys():
            print(addr_client)
            user = User()
            user.set_user(connection_socket.recv(4096).decode(), addr_client)
            connections[addr_client] = user
            addresses[user] = addr_client
            sock[user] = connection_socket
            print(user.username)
        # Find to whom the message is for and send
        sentence = connection_socket.recv(4096).decode()
        print('the sentence is' + sentence)
        if sentence == '<get_users>':
            connected_user = connections[addr_client].connected_user
            connection_socket.sendto(bytes(str(connections).encode()), addresses[connected_user])
        elif sentence == '<connect_bar1>':
            print('here')
            for connection in connections.values():
                print(connection)
                if connection.username == 'bar1':
                    print('1')
                    newsock = sock[connection]
                    print('2')
              #      print(newsock)
              #      connections[connection].connect(connections[addr_client])
                    print('3')
            print(addresses[connections[addr_client].connected_user])
            print('5')
            connection_socket.sendto(bytes('connected!'.encode()),addr_client)
            print('success')
        else:
            connected_user = connections[addr_client].connected_user
            sentencefrom = connections[addr_client].username + ': '
            print(sentencefrom + sentence)
            if addr_client != addresses[connected_user]:
                connection_socket.sendto(bytes('\nSent!\n'.encode()), addr_client)
            newsock.send(bytes(sentencefrom.encode() + sentence.encode()))
            print(addr_client)
            print(addresses[connected_user])


# ThreadPool run 5 threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    clients = [executor.submit(run) for _ in range(5)]
