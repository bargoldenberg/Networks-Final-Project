# import socket
from socket import *
import time


class Client:
    def __init__(self):
        serverName = '127.0.0.1'
        serverPort = 1234
        udpserverport = 1235
        self.SERVER_ADDRESS = (serverName, serverPort)
        self.UDP_SERVER_ADRESS = (serverName,udpserverport)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.udpclientsocket = socket(AF_INET,SOCK_DGRAM)
        self.clientSocket.connect(self.SERVER_ADDRESS)
        #self.udpclientsocket.connect(self.UDP_SERVER_ADRESS)
        self.username = None

    def init_connect(self, username):
        self.clientSocket.send(username.encode())

    def checksum(self,data):
        pos = len(data)
        if (pos & 1):  # If odd...
            pos -= 1
            sum = ord(data[pos])  # Prime the sum with the odd end byte
        else:
            sum = 0

        # Main code: loop to calculate the checksum
        while pos > 0:
            pos -= 2
            sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

        sum = (sum >> 16) + (sum & 0xffff)
        sum += (sum >> 16)

        result = (~ sum) & 0xffff  # Keep lower 16 bits
        result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
        return chr(result / 256) + chr(result % 256)

    def send_message(self, message):
        if message == 'File.txt':
            File = open('recvFile.txt', 'w')
            self.udpclientsocket.sendto('gimmie a file'.encode(),self.UDP_SERVER_ADRESS)
            self.udpclientsocket.settimeout(1)
            while True:
                try:
                    data = self.udpclientsocket.recv(4096).decode()
                    #print(data)
                    header = data.split(';')
                    #print(header)
                    seq = header[0]
                    checksum = header[1]
                    payload = ''
                    i=2
                    while i < len(header):
                        if len(header) == 3 or i == len(header)-1:
                            payload += header[i]
                            i+=1
                        else:
                            payload +=header[i]+';'
                            i+=1
                    print(payload)
                    # if checksum!=self.checksum(payload):
                    #     self.udpclientsocket.sendto(('NAK'+str(seq)).encode(),self.UDP_SERVER_ADRESS)
                    # else:
                    #     self.udpclientsocket.sendto(('ACK'+str(seq)).encode(), self.UDP_SERVER_ADRESS)
                    print('1')
                    File.write(payload)
                    print('2')
                except:
                    File.close()
                    break
            return
        # if self.username is None:
        #     self.username = input('Input Username:')
        #     self.init_connect(self.username)
        time.sleep(0.5)
        self.clientSocket.send(message.encode())

    def receive_message(self):
        self.clientSocket.settimeout(0.2)
        try:
            message = self.clientSocket.recv(4096)
            if message.decode() != '':
                return message.decode()
        except:
            return

    def end_connection(self):
        self.clientSocket.close()
