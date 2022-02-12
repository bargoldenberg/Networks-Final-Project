# import socket
from socket import *
import time


class Client:
    def __init__(self):
        print('hi')
        serverName = 'localhost'
        serverPort = 55009
        self.SERVER_ADDRESS = (serverName, serverPort)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.SERVER_ADDRESS)
        self.username = None
        print('hi2')

    def init_connect(self, username):
        self.clientSocket.send(username.encode())

    def send_message(self, message):
        if self.username is None:
            self.username = input('Input Username:')
            self.init_connect(self.username)
        time.sleep(0.5)
        #self.clientSocket.settimeout(0.2)
        #self.clientSocket = socket(AF_INET, SOCK_STREAM)
        #self.clientSocket.connect(self.SERVER_ADDRESS)
        self.clientSocket.send(message.encode())

    def receive_message(self):
        message = self.clientSocket.recv(4096)
        if message.decode() != '':
            print(message.decode())

    def end_connection(self):
        self.clientSocket.close()
