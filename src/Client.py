# import socket
import os
from socket import *
import time
import pickle



class Client:
    def __init__(self):
        serverName = '127.0.0.1'
        serverPort = 55000
        udpserverport = 55001
        self.SERVER_ADDRESS = (serverName, serverPort)
        self.UDP_SERVER_ADRESS = (serverName, udpserverport)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.udpclientsocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.connect(self.SERVER_ADDRESS)
        # self.udpclientsocket.connect(self.UDP_SERVER_ADRESS)
        self.username = None

    def init_connect(self, username):
        self.clientSocket.send(username.encode())

    def send_message(self, message):
        format = self.check_format(message)  # Checking the format of the message -> asking for file or normal message.
        print("Format: ", format)
        size = None
        if format == 1:  # 1 is asking for file (means it ends with .txt/.png/ .jpg), 0 is normal message.
            File = open(os.path.abspath(os.path.join('..','Downloads',message)), 'wb')  # Change to the message's name
            while True:
                self.udpclientsocket.settimeout(3)
                try:
                    self.udpclientsocket.sendto(message.encode(), self.UDP_SERVER_ADRESS)
                    print("Client: create connection with the server, Asking for ", message)
                    size = int(self.udpclientsocket.recv(65000).decode())
                    if size is not None:
                        self.udpclientsocket.settimeout(None)
                        break
                except:
                    continue
            all_data = {}
            print("Packets Size: ", size, "All Data Size: ", len(all_data))
            print("...")
            time.sleep(1)
            # self.udpclientsocket.settimeout(10)
            while True:
                while len(all_data) < size:
                    try:
                        print("Client: waiting for data from the Server")
                        data = self.udpclientsocket.recv(65000)
                        packet = pickle.loads(data)
                        seq = packet[0]
                        payload = packet[1]
                        print("Client: Packet (seq num: ", seq, ") received, sending ACK ")
                        all_data[seq] = payload
                        self.udpclientsocket.sendto(('ACK' + str(seq)).encode(), self.UDP_SERVER_ADRESS)
                        print('all_data length: ',len(all_data),', size: ',size)
                    except:
                        File.close()
                        break
                sorted_data = {}
                for key in sorted(all_data):
                    sorted_data[key]=all_data[key]
                for pckt in sorted_data.values():
                    File.write(pckt)
                print("Download Finished.")
                for _ in range(10):
                    print('sending download  finished')
                    self.udpclientsocket.sendto('Download Finished'.encode(),self.UDP_SERVER_ADRESS)
                File.close()
                return
        time.sleep(0.5)
        self.clientSocket.send(message.encode())

    def check_format(self, message: str):
        f = ''
        i = len(message) - 1
        while message[i] != '.' and i > 0:
            i -= 1
        f = message[i:]
        if f == '.txt' or f == '.png' or f == '.jpg' or f == '.gif' or f == '.mp3' or f =='.mp4':
            return 1
        else:
            return 0

    def receive_message(self):
        #self.clientSocket.settimeout(0.2)
        try:
            message = self.clientSocket.recv(4096)
            if message.decode() != '':
                return message.decode()
        except:
            return

    def end_connection(self):
        self.udpclientsocket.close()
        self.clientSocket.close()

