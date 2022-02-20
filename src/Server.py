# import socket
from socket import *
import concurrent.futures
from User import *
from scapy import all
import threading
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
        self.SERVER_ADDRESS = ('10.9.4.127', 55002)
        self.SERVER_ADDRESS_UDP = ('10.9.4.127', 55003)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket_udp = socket(AF_INET,SOCK_DGRAM)
        self.connections = {}
        self.sock = {}
        self.serverSocket.bind(self.SERVER_ADDRESS)
        self.serverSocket_udp.bind(self.SERVER_ADDRESS_UDP)
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
    def msg_all(self,sentence,connection_socket,addr_client):
        FLAG = True
        if sentence[:9] == '<msg_all>':
            FLAG = False
            for socket in self.sock.values():
                if socket != connection_socket:
                    sentencefrom = self.connections[addr_client].username + ': '
                    socket.send(bytes((sentencefrom+sentence[9:]).encode()))
        return FLAG
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
            FLAG = self.msg_all(sentence,connection_socket,addr_client)
            if sentence == '<get_users>':
                connection_socket.send(bytes(str(self.connections).encode()))
            else:
                if FLAG:
                    sentencefrom = self.connections[addr_client].username + ': '
                    print(sentencefrom + sentence)
                    connection_socket.send(bytes('Sent!\n'.encode()))
                    self.connections[addr_client].connected_user.send(bytes(sentencefrom.encode() + sentence.encode()))

    def create_pkt(self,data,SEGMENTSIZE,offset,size):
        if SEGMENTSIZE+offset>size:
            return data[offset:]
        else:
            return data[offset:offset+SEGMENTSIZE]

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
        return chr(int(result / 256)) + chr(result % 256)

    def segment(self,data,size):
        packets = []
        SEGMENTSIZE = 5
        OFFSET=0
        seq = 0
        while OFFSET<=size:
            payload = self.create_pkt(data, SEGMENTSIZE, OFFSET, size)
            check_sum = self.checksum(payload)
            packets.append(f'{seq};{check_sum};{payload}')
            seq+=1
            OFFSET+=SEGMENTSIZE
        return packets

    def run_udp(self):
        while True:
            message, clientaddress = self.serverSocket_udp.recvfrom(4096)
            file = open('/home/bar/PycharmProjects/Networks-Final-Project/Data/File.txt','r')
            data = file.read()
            packets = self.segment(data,len(data))
            print(packets)
            for packet in packets:
                self.serverSocket_udp.sendto(packet.encode(),clientaddress)
            print(data)
    def listen(self):
        while True:
            print(self.serverSocket_udp.recv(4096).decode())

# ThreadPool run 5 threads
if __name__ == '__main__':
    server = Server()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        clients = [executor.submit(server.run) for _ in range(5)]
        udp_clients = [executor.submit(server.run_udp) for _ in range(5)]
    # t = threading.Thread(target = server.listen,args =[])
    # t.start
    # t.join