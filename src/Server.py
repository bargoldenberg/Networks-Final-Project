# import socket
import math
import os
import time
from socket import *
import concurrent.futures
# from tkinter import Image
from PIL import Image
from src.User import *
from scapy import all
import threading
import pickle
import time


'''
    Left to do:
        - Implement RDT (add timeout)
        - add Congestion Control to window size
        - add user list to GUI
    How it works so far:
        - When a client connects to the server he sends his name first that 
          gets appended to the connections dictionary including his connection socket.
          Then he chooses who to talk to (he himself is default),
          he sends a message to the server who sends the message through the socket to whom he wants
          to communicate with.
          Each client is a thread in the server 
          
'''

class Server():
    def __init__(self,addr,tcp_port,udp_port):
        self.SERVER_ADDRESS = (addr, tcp_port)
        self.SERVER_ADDRESS_UDP = (addr, udp_port)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket_udp = socket(AF_INET,SOCK_DGRAM)
        self.ack_received = []
        self.connections = {}
        self.sock = {}
        self.serverSocket.bind(self.SERVER_ADDRESS)
        self.serverSocket_udp.bind(self.SERVER_ADDRESS_UDP)
        self.serverSocket.listen(5)
        self.timeout = None
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
                print("Client Address: ",addr_client)
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
                    #connection_socket.send(bytes('Sent!\n'.encode()))
                    self.connections[addr_client].connected_user.send(bytes(sentencefrom.encode() + sentence.encode()))
    '''
    The Next five functions are Helpers for the selective repeat UDP.
    '''
    # cut our data to small packets -  each run it starts from offset to offset +  SEGMENTSIZE
    def create_pkt(self,data:bytes,SEGMENTSIZE,offset,size):
        if SEGMENTSIZE+offset>size:
            return data[offset:]
        else:
            return data[offset:offset+SEGMENTSIZE]
    # Create Segment By Bytes
    def segment_bytes(self,data:bytes,size):
        print("Segment values:")
        packets = [] # List that contain all the packets.
        SEGMENTSIZE = 507   # Will Be Changes.
        OFFSET = 0
        seq = 0
        while OFFSET<=size:
            buffer = [] ### ----> for making a bytes list
            payload = self.create_pkt(data, SEGMENTSIZE, OFFSET, size)
            print('Payload Format: ', type(payload))
            # check_sum = self.checksum(payload).encode()
            # print('CheckSum Format: ', type(check_sum))
            # print('Seq: ',seq,', Byte seq: ',seq.to_bytes())
            buffer.append(seq)
            # buffer[1]= self.checksum(payload).encode()
            buffer.append(payload)
            packets.append(buffer)
            seq+=1
            OFFSET+=SEGMENTSIZE
        return packets
    '''
    Test Functions For Sappir's Implementation
    '''
    def run_udp_Final(self):
        window_size = 4
        while True:
            print('hi')
            self.serverSocket_udp.settimeout(None)
            try:
                message, clientaddress = self.serverSocket_udp.recvfrom(4096)
            except:
                continue
            print("messege:",message.decode())
            if self.message_type(message.decode()) == 1:
                print('Server: Ack reseived ->',message.decode())
            elif self.message_type(message.decode()) == 0:
                path = "../Data/"
                path += str(message.decode())
                print('Path = ',path)
                if os.path.exists(path) == True:
                    print("File Name: ",message.decode())
                    w_start = 0
                    sent = []
                    expected_acks = {}
                    file = open(path, 'rb')
                    data = file.read()
                    print('Data = ',data)
                    packets = self.segment_bytes(data, len(data))
                    print("Server: Data split to packets:  -->", packets)
                    # Sending the packets size --> as String
                    self.serverSocket_udp.sendto((str(len(packets))).encode(),clientaddress)
                    while w_start < len(packets):
                        print("w_start:", w_start , ', Length Packets:',len(packets))
                        for i in range(window_size):
                            curr = i + w_start
                            print(sent)
                            if curr not in sent and curr <= len(packets):
                                sent.append(curr)
                                if curr> len(packets)-1:
                                    break
                                print('Length before pickle',len(packets[curr][1]))
                                print('payload seq: ',packets[curr][0],'payload: ',packets[curr][1])
                                toSend = pickle.dumps(packets[curr])
                                print(len(toSend))
                                self.serverSocket_udp.sendto(toSend, clientaddress)
                                print("Server: Packet ", curr, " Sent")
                                tmp = 'ACK'
                                tmp += str(curr)
                                expected_acks[curr] = tmp
                        # self.serverSocket_udp.settimeout(1)
                        try:
                            message, clientaddress = self.serverSocket_udp.recvfrom(4096)
                        except:
                            pass
                        finally:
                            print('Server: new Message: ',message.decode())
                            if self.message_type(message.decode()) == 1:
                                print('Server: Ack reseived ->',message.decode())
                                print("Ack received:", message.decode())
                            '''
                            While Loop For Lost Packets, For each packet that the server has not received an Ack for (From Client)
                                It will resend this packet and Wont move Forward in the sending. 
                            '''
                            while expected_acks[w_start] not in self.ack_received:
                                print("Server: Missing Ack",w_start, ', Resending Packet.')
                                print('Server: Ack Received:',self.ack_received)
                                toSend = pickle.dumps(packets[w_start])
                                print('Packets:',packets[w_start])
                                print('Index',w_start)
                                start = time.time()
                                self.serverSocket_udp.sendto(toSend, clientaddress)
                                try:
                                    if self.timeout is None:
                                        self.serverSocket_udp.settimeout(3)
                                    else:
                                        self.serverSocket_udp.settimeout(self.timeout)
                                    message,_ = self.serverSocket_udp.recvfrom(4096)
                                    if message.decode() == 'Download Finished':
                                        return
                                    print('msg',message.decode())
                                    if self.message_type(message.decode()) == 1:
                                        end = time.time()
                                        self.timeout = end-start+0.3
                                        print('Server: Ack reseived (After ReSending)->',message.decode())
                                except:
                                    print("Server: No Ack received For Packet ",w_start,"Resending Packet.")
                                    continue
                            '''
                            Ack's Returned Goes Here.
                            '''
                            w_start += 1
                            w_end = w_start + window_size
                            # self.serverSocket_udp.settimeout(1)
                    print(self.ack_received)
                    print("Server: Sending Finished.")
                else:
                    print("Path/File is not exist")
            else:
                print("Wrong File name, Try Again.")
    def message_type(self,message):
        if message[0] == 'A' and message[1] == 'C' and message[2] == 'K':
            if message not in self.ack_received:
                self.ack_received.append(message)
            return 1
        elif message[0] == 'N' and message[1] == 'A' and message[2] == 'C' and message[2] == 'K':
            return -1
        else:
            return 0

# ThreadPool run 5 threads
    def run_server(self,addr,tcpport,udport):
        server = Server(addr,tcpport,udport)
        clients = []
        udp_clients = []
        for i in range(5):
            t = threading.Thread(target=server.run,args = [])
            if i == 1:
                t1 = threading.Thread(target = server.run_udp_Final,args = [])
                udp_clients.append(t1)
            clients.append(t)
        for thread in clients:
            thread.start()
        for thread in udp_clients:
            thread.start()
