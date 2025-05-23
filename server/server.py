from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('chat_message')
def handle_chat_message(data):
    print('Received message:', data)
    socketio.emit('chat_message', data)

if __name__ == '__main__':
    socketio.run(app, port=5000)
