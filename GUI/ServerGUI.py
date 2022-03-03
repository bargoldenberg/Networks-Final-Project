import subprocess
import tempfile

import kivy.uix.image
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import os
import sys
from subprocess import run


import time
sys.path.append(os.path.abspath(os.path.join('..')))
from src.Server import *



class Chat(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.running = Label(text='SERVER RUNNING', font_size=90, color='#FFD043')
        self.add_widget(self.running)
        self.end = Button(text='END SERVER', size_hint=(0.7, 0.3), bold=True, background_color='#FFD043',
                             background_normal='', color='#00000')
        self.end.bind(on_press=self.end_server)
        self.add_widget(self.end)

    def end_server(self,instance):
        server_app.server.end_server()
        App.get_running_app().stop()


class login_screen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.window = GridLayout()
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(kivy.uix.image.Image(source='SBC.png'))
        self.addresstext = Label(text='ENTER ADDRESS', font_size=20, color='#FFD043')
        self.add_widget(self.addresstext)
        self.address = TextInput(text='127.0.0.1',multiline=False, padding_y=(20, 20), size_hint=(1, 1.2))
        self.add_widget(self.address)
        self.porttcptext = Label(text='ENTER TCP PORT', font_size=20, color='#FFD043')
        self.add_widget(self.porttcptext)
        self.tcpport = TextInput(text='55002', multiline=False, padding_y=(20, 20), size_hint=(1, 1.2))
        self.add_widget(self.tcpport)
        self.portudptext = Label(text='ENTER UDP PORT', font_size=20, color='#FFD043')
        self.add_widget(self.portudptext)
        self.udpport = TextInput(text='55003',multiline=False, padding_y=(20, 20), size_hint=(1, 1.2))
        self.add_widget(self.udpport)

        self.button = Button(text='START SERVER', size_hint=(1, 1), bold=True, background_color='#FFD043',
                             background_normal='', color='#00000')
        self.button.bind(on_press=self.start)
        self.add_widget(self.button)
        # return self

    def start(self, instance):
        # Server.run_server(None,self.address.text,int(self.tcpport.text),int(self.udpport.text))
        server_app.server = Server.run_server(None,self.address.text, int(self.tcpport.text), int(self.udpport.text))
        server_app.screen_manager.current = 'log'


class ServerApp(App):
    def build(self):
        # return login_screen()
        self.screen_manager = ScreenManager()
        self.login_screen = login_screen()
        screen = Screen(name='login')
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)
        self.chat_screen = Chat()
        screen = Screen(name='log')
        screen.add_widget(self.chat_screen)
        self.screen_manager.add_widget(screen)
        self.server = None
        return self.screen_manager

if __name__ == '__main__':
    server_app = ServerApp()
    server_app.run()