from Client import *


class User:
    def __init__(self):
        self.username = ''
        self.address = ''
        self.connected_user = self

    def set_user(self, username, address):
        self.username = username
        self.address = address

    def connect(self, user):
        self.connected_user = user


if __name__ == '__main__':
    client = Client()
    while True:
        message = input('Enter Message: ')
        client.send_message(message)
        client.receive_message()
    client.end_connection()
