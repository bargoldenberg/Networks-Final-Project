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
        print('start1')
        server = Server.run_one_thread(Server, '127.0.0.1', 55002, 55003)
        client = Client()
        file = 'file.txt'
        wrongfile = 'file.txs'
        self.assertEqual(client.check_format(file),1)
        self.assertNotEqual(client.check_format(wrongfile),1)
        for i in range(2):
            client.send_message('kill_server')
        time.sleep(1)
        client.end_connection()
        print('end1')

    def test_recieve_msg(self):
        time.sleep(1)
        print('start2')
        server = Server.run_one_thread(Server, '127.0.0.1', 55002, 55003)
        client = Client()
        client.init_connect('test')
        client.send_message('hi')
        x = None
        while x is None:
            x = self.client.receive_message()
        self.assertEqual('hi',x.split(':')[1][1:])
        for i in range(2):
            client.send_message('kill_server')
        time.sleep(1)

        client.end_connection()
        print('end2')


    def test_recieve_file(self):
        print('start3')
        time.sleep(1)
        server = Server.run_one_thread(Server, '127.0.0.1', 55002, 55003)
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
        for i in range(2):
            client.send_message('kill_server')
        time.sleep(1)
        client.end_connection()
        print('end3')

        
    def test_segment_bytes(self):
        print('start4')
        time.sleep(1)
        server = Server.run_one_thread(Server, '127.0.0.1', 55002, 55003)
        client = Client()
        original_file = open(os.path.abspath(os.path.join('..', 'Data', 'rdt.gif')), 'rb')
        original_data = original_file.read()
        packets = server.segment_bytes(original_data,len(original_data))
        self.assertEqual(len(packets),int(len(original_data)/32000)+1)
        original_file.close()
        for i in range(2):
            client.send_message('kill_server')
        time.sleep(1)
        client.end_connection()
        print('end4')

if __name__ == '__main__':
    unittest.main()
