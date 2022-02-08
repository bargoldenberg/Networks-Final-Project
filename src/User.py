from Client import *
import time
class User:
    def __init__(self):
        self.username = ''
        self.address = ''
        self.connected_user = self
    def set_user(self,username,adress):
        self.username=username
        self.address=adress
    def connect(self,user):
        self.connected_user=user
if __name__ == '__main__':
    while True:
        client = Client()
        message = input('Enter Message: ')
        client.send_message(message)
        client.receive_message()
    client.end_connection()
