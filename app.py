from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

# Index route renders the chat page
@app.route('/')
def index():
    return render_template('index.html')

# Listen for messages from clients and broadcast them to everyone in the room
@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
