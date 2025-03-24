from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages for new users to see past messages
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_msg = {'username': session.get('username', 'Anonymous'), 'text': msg, 'time': timestamp}
    messages.append(formatted_msg)
    send(formatted_msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    send({'messages': messages}, json=True)

@app.route('/set_username', methods=['POST'])
def set_username():
    session['username'] = request.form['username']
    return "", 204

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
