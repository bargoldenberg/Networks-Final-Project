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
import time
sys.path.append(os.path.abspath(os.path.join('..')))
from src.User import *
from src.Client import *

class Files(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.window = GridLayout()
        self.cols = 3
        self.rows = 3
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.File = Button(text='File.txt', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                             background_normal='', color='#00000')
        self.File.bind(on_press=self.textfile)
        self.add_widget(self.File)
        self.meme1 = Button(text='meme1.jpg', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                             background_normal='', color='#00000')
        self.meme1.bind(on_press=self.meme1dwn)
        self.add_widget(self.meme1)

        self.meme2 = Button(text='meme2.jpg', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                            background_normal='', color='#00000')
        self.meme2.bind(on_press=self.meme2dwn)
        self.add_widget(self.meme2)

        self.rdt_b = Button(text='rdt.gif', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                            background_normal='', color='#00000')
        self.rdt_b.bind(on_press=self.rdt)
        self.add_widget(self.rdt_b)

        self.pc = Button(text='computer.gif', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                            background_normal='', color='#00000')
        self.pc.bind(on_press=self.computer)
        self.add_widget(self.pc)

        self.return_to_chat = Button(text='RETURN', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                            background_normal='', color='#00000')
        self.return_to_chat.bind(on_press=self.goback)
        self.add_widget(self.return_to_chat)

    def textfile(self,instance):
        chat_app.user.send_message(chat_app.client, 'File.txt')
    def meme1dwn(self,instance):
        chat_app.user.send_message(chat_app.client, 'meme1.jpg')
    def meme2dwn(self,instance):
        chat_app.user.send_message(chat_app.client,'meme2.jpg')
    def rdt(self,instance):
        chat_app.user.send_message(chat_app.client,'rdt.gif')
    def computer(self,instance):
        chat_app.user.send_message(chat_app.client,'computer.gif')
    def goback(self,instance):
        chat_app.screen_manager.current = 'chat'


        # return self

class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        #self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)
        #self.chat_history.text_size = (300, None)
    def update_chat_history_layout(self,_=None):
        self.layout.height = self.chat_history.texture_size[1]+15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98,None)

class Chat(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.history = ScrollableLabel(height=Window.size[1] * 0.9, size_hint_y=None)
        self.add_widget(self.history)
        self.new_message = TextInput(width=Window.size[0] * 0.6, size_hint_x=None, multiline=False)
        self.send = Button(text='SEND',size_hint=(0.3, 1), bold=True, background_color='#FFD043', background_normal='', color='#00000')
        self.send.bind(on_press=self.send_message)
        self.download = Button( text = 'FILES',size_hint = (0.3,1), bold =True, background_color= '#FFD043', background_normal='', color = '#00000')
        self.download.bind(on_press = self.download_screen)
        bottom_line = GridLayout(cols=3)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.download)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)
        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_once(self.focus_text_input,1)
        chat_app.user.listen(chat_app.client,self.incoming_message)
        self.bind(size = self.adjust_fields)

    def download_screen(self,instance):
        chat_app.screen_manager.current = 'download'


    def adjust_fields(self,*_):
        if Window.size[1]*0.1<50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1]*0.9
        self.history.height = new_height

        if Window.size[0]*0.2<160:
            new_width = Window.size[0]-160
        else:
            new_width = Window.size[0]*0.8
        self.new_message.width = new_width

        Clock.schedule_once(self.history.update_chat_history_layout,0.01)
    def on_key_down(self,instance,keyboard,keycode,text,modifiers):
        if keycode==40:
            self.send_message(None)
    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ''
        if message:
            self.history.update_chat_history(f'[color=FFD043]{chat_app.login_screen.username}[/color]>{message}')
            #user = User()
            chat_app.user.send_message(chat_app.client, message)
        Clock.schedule_once(self.focus_text_input, 0.1)
    def focus_text_input(self,_):
        self.new_message.focus=True
    def incoming_message(self, username, message):
        print('hi')
        self.history.update_chat_history(f"[color=439bff]{username}[/color]{message}")

class login_screen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.window = GridLayout()
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(Image(source='SBC.png'))
        self.usertext = Label(text='Enter Username', font_size=20, color='#FFD043')
        self.add_widget(self.usertext)
        self.user = TextInput(multiline=False, padding_y=(20, 20), size_hint=(1, 0.5))
        self.add_widget(self.user)
        self.button = Button(text='LOGIN', size_hint=(1, 0.5), bold=True, background_color='#FFD043',
                             background_normal='', color='#00000')
        self.button.bind(on_press=self.login)
        self.add_widget(self.button)
        # return self

    def login(self, instance):
        Clock.schedule_once(self.connect, 1)
        chat_app.screen_manager.current = 'chat'

    def connect(self, _):
        self.username = self.user.text
        chat_app.user.run(self.username, chat_app.client)

class SBChatApp(App):
    def build(self):
        # return login_screen()
        self.screen_manager = ScreenManager()
        self.client = Client()
        self.login_screen = login_screen()
        screen = Screen(name='login')
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)
        self.user = User()
        self.chat_screen = Chat()
        screen = Screen(name='chat')
        screen.add_widget(self.chat_screen)
        self.screen_manager.add_widget(screen)
        self.download_screen = Files()
        screen = Screen(name = 'download')
        screen.add_widget(self.download_screen)
        self.screen_manager.add_widget(screen)
        return self.screen_manager

if __name__ == '__main__':
    chat_app = SBChatApp()
    chat_app.run()
