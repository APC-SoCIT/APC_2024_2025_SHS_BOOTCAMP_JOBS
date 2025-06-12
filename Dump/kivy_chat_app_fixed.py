
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import threading
from websocket import WebSocketApp

class ChatClient:
    def __init__(self, ui):
        self.ui = ui
        self.connected = False
        self.ws = WebSocketApp("ws://localhost:8765",
                               on_open=self.on_open,
                               on_close=self.on_close,
                               on_error=self.on_error,
                               on_message=self.on_message)
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def on_open(self, ws):
        self.connected = True
        print("WebSocket connection established.")

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        print("WebSocket connection closed.")

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_message(self, ws, message):
        self.ui.update_chat(f"Friend: {message}")

    def send(self, message):
        if self.connected:
            self.ws.send(message)
        else:
            print("Not connected. Message not sent.")

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.messages = Label(size_hint_y=8)
        self.add_widget(self.messages)
        self.input = TextInput(size_hint_y=1, multiline=False)
        self.add_widget(self.input)
        self.send_button = Button(text='Send', size_hint_y=1)
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)
        self.client = ChatClient(self)

    def send_message(self, instance):
        msg = self.input.text.strip()
        if msg:
            self.update_chat(f"You: {msg}")
            self.client.send(msg)
            self.input.text = ""

    def update_chat(self, message):
        self.messages.text += f"\n{message}"

class ChatApp(App):
    def build(self):
        return ChatUI()

if __name__ == '__main__':
    ChatApp().run()
