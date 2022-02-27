# import socket
from socket import *
import time
import pickle



class Client:
    def __init__(self):
        serverName = '127.0.0.1'
        serverPort = 55002
        udpserverport = 55003
        self.SERVER_ADDRESS = (serverName, serverPort)
        self.UDP_SERVER_ADRESS = (serverName, udpserverport)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.udpclientsocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.connect(self.SERVER_ADDRESS)
        # self.udpclientsocket.connect(self.UDP_SERVER_ADRESS)
        self.username = None

    def init_connect(self, username):
        self.clientSocket.send(username.encode())

    def checksum(self, data):
        data = str(data)
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
        return chr(int(result / 256)) + chr(result % 256)

    def send_message(self, message):
        format = self.check_format(message)  # Checking the format of the message -> asking for file or normal message.
        print("Format: ", format)
        if format == 1:  # 1 is asking for file (means it ends with .txt/.png/ .jpg), 0 is normal message.
            File = open(message, 'wb')  # Change to the message's name
            self.udpclientsocket.sendto(message.encode(), self.UDP_SERVER_ADRESS)
            print("Client: create connection with the server, Asking for ", message)
            size = int(self.udpclientsocket.recv(4096).decode())
            all_data = {}
            print("Packets Size: ", size, "All Data Size: ", len(all_data))
            print("...")
            time.sleep(1)
            # self.udpclientsocket.settimeout(10)
            while True:
                while len(all_data) < size:
                    try:
                        print("Client: waiting for data from the Server")
                        data = self.udpclientsocket.recv(4096)
                        print('Client: Data = ',data)
                        packet = pickle.loads(data)
                        print("Client: Packet = ", packet)
                        seq = packet[0]
                        payload = packet[1]
                        print('Length after pickle',len(payload))
                        print('payload seq: ',seq,'payload: ',payload)
                        print("Client: Packet (seq num: ", seq, ") received, sending ACK ")
                        all_data[seq] = payload
                        self.udpclientsocket.sendto(('ACK' + str(seq)).encode(), self.UDP_SERVER_ADRESS)
                    except:
                        File.close()
                        break
                for pckt in all_data.values():
                    File.write(pckt)
                print("Finished: ", all_data)
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
        if f == '.txt' or f == '.png' or f == '.jpg' or f == '.gif':
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
        self.clientSocket.close()
