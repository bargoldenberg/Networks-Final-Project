
import threading
import time


class User:
    def __init__(self):
        self.username = ''
        self.address = ''
        self.connected_user = None
        self.stop = False
        self.t2 = None
        self.t = None

    def set_user(self, username, address):
        self.username = username
        self.address = address

    def connect(self, socket):
        self.connected_user = socket

    def __repr__(self):
        return f"UserName = {self.username}"

    def start_connection(self,client,username):

        client.send_message(username)
        client.send_message('connected')
        try:
            client.send_message('<msg_all>has connected to the chat!')
        except:
            pass
    def receive_message(self,client,update_message):
        while True:
            if self.stop:
                print('stopped')
                break

            message = client.receive_message()
            if message is None:
                continue
            else:
                if message.startswith('{'):
                    update_message('SERVER',message)
                else:
                    breakdown = message.split(':')
                    name = breakdown[0]
                    if len(breakdown)>1:
                        msg = breakdown[1]
                        update_message(name,msg)
                    else:
                        update_message(name,'')

    def send_username(self,client,username):
        self.start_connection(client,username)
        # while True:
        #     message = input()
        #     if message == '<end_connection>':
        #         break
        #     client.send_message(message)
        # client.end_connection()
    def send_message(self,client,message):
        if message == '<end_connection>':
            client.send_message(message)
            self.stop = True
            print('joining')
            self.t.join()
            client.end_connection()
            return
        client.send_message(message)



    def run(self,username,client):
        #t1 = threading.Thread(target=self.receive_message,args=[client,None])
        self.t2 = threading.Thread(target=self.send_username,args=[client,username])
        #t1.start()
        self.t2.start()
        # self.t2.join()
        # t1.join()
        pass
    def listen(self,client,update_message):
        self.t = threading.Thread(target = self.receive_message,args = [client,update_message])
        self.t.start()
        #t.join()
