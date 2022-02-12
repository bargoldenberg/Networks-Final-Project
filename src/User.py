from Client import *
import threading

class User:
    def __init__(self):
        self.username = ''
        self.address = ''
        self.connected_user = None

    def set_user(self, username, address):
        self.username = username
        self.address = address

    def connect(self, socket):
        self.connected_user = socket

    def __repr__(self):
        return f"UserName = {self.username}"

def receive_message(client):
    while True:
        client.receive_message()
def send_message(client):
    while True:
        message = input()
        if message == '<end_connection>':
            break
        client.send_message(message)
    client.end_connection()


if __name__ == '__main__':
    client = Client()
    t1 = threading.Thread(target=receive_message,args=[client])
    t2 = threading.Thread(target=send_message,args=[client])
    t1.start()
    t2.start()
    t1.join()
    t2.join()

