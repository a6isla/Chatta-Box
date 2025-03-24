from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS # type: ignore
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("User connected!")

@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected!")

@socketio.on('message')
def handle_message(message):
    print(f"Message: {message}")
    emit('response', {'data': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)