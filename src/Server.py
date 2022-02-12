# import socket
from socket import *
import concurrent.futures
from User import *

'''
    Left to do:
        - Send message to all users.
        - GUI
        - Finish all commands.
    How it works so far:
        - When a client connects to the server he sends his name first that 
          gets appended to the connections dictionary including his connection socket.
          Then he chooses who to talk to (he himself is default),
          he sends a message to the server who sends the message through the socket to whom he wants
          to communicate with.
          Each client is a thread in the server (we used threadpools)
          
'''
class Server():
    def __init__(self):
        self.SERVER_ADDRESS = ('', 55017)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.connections = {}
        self.sock = {}
        self.serverSocket.bind(self.SERVER_ADDRESS)
        self.serverSocket.listen(5)
        print("The server is ready to receive clients")

    def connect(self,sentence,connection_socket,addr_client):
        if sentence[:9] == '<connect_' and sentence[len(sentence) - 1:len(sentence)] == '>':
            for connection in self.connections.values():
                print(connection)
                print(sentence[len(sentence) - 1:len(sentence)])
                print(sentence[9:len(sentence)])
                if connection.username == sentence[9:len(sentence) - 1]:
                    self.connections[addr_client].connected_user = self.sock[connection]
                    connection.connected_user = connection_socket
            connection_socket.send(bytes('connected!'.encode()))

    def run(self):
        connection_socket, addr_client = self.serverSocket.accept()
        while True:
            if addr_client not in self.connections.keys():
                print(addr_client)
                user = User()
                user.set_user(connection_socket.recv(4096).decode(), addr_client)
                self.connections[addr_client] = user
                self.sock[user] = connection_socket
                user.connected_user = connection_socket
                print(user.username)
            # Find to whom the message is for and send
            sentence = connection_socket.recv(4096).decode()
            print('the sentence is ' + sentence)
            self.connect(sentence, connection_socket, addr_client)
            if sentence == '<get_users>':
                connection_socket.send(bytes(str(self.connections).encode()))
            else:
                sentencefrom = self.connections[addr_client].username + ': '
                print(sentencefrom + sentence)
                connection_socket.send(bytes('Sent!\n'.encode()))
                self.connections[addr_client].connected_user.send(bytes(sentencefrom.encode() + sentence.encode()))


# ThreadPool run 5 threads
if __name__ == '__main__':
    server = Server()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        clients = [executor.submit(server.run) for _ in range(5)]
