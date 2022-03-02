import unittest
import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join('..')))
from src.User import *
from src.Client import *
from src.Server import *

class ClientTests(unittest.TestCase):
    def test_check_format(self):
        file = 'file.txt'
        wrongfile = 'file.txs'
        self.assertEqual(Client.check_format(Client,file),1)
        self.assertNotEqual(Client.check_format(Client,wrongfile),1)
    def test_recieve_msg(self):
        server = Server.run_one_thread(Server,'127.0.0.1',55000,55001)
        client = Client()
        client.init_connect('test')
        client.send_message('hi')
        x = None
        while x is None:
            x = client.receive_message()
        self.assertEqual('hi',x.split(':')[1][1:])
        client.send_message('kill_server')
        client.end_connection()

    def test_recieve_file(self):
        server = Server.run_one_thread(Server,'127.0.0.1',55000,55001)
        client = Client()
        client.init_connect('test')
        time.sleep(2)
        client.send_message('rdt.gif')
        file = open(os.path.abspath(os.path.join('..','Downloads','rdt.gif')),'rb')
        data = file.read()
        original_file = open(os.path.abspath(os.path.join('..','Data','rdt.gif')),'rb')
        original_data = original_file.read()
        self.assertEqual(data,original_data)
        file.close()
        original_file.close()
        client.send_message('kill_server')
        client.end_connection()
        

if __name__ == '__main__':
    unittest.main()