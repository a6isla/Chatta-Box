from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# PostgreSQL setup
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("User connected!")
    # Send past messages to new user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10')
    messages = cursor.fetchall()
    conn.close()
    for message in messages:
        emit('response', {'username': message[1], 'message': message[2]})

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    # Save message to database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (username, message) VALUES (%s, %s)', (username, message))
    conn.commit()
    conn.close()
    # Broadcast to all users
    emit('response', {'username': username, 'message': message}, broadcast=True)

@socketio.on('join')
def handle_join(username):
    print(f"User {username} joined the chat!")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
