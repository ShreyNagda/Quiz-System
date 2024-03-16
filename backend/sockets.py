import requests
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from app import app

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(data, room):
    print(data, room)
    send(data, to=room, broadcast=True, include_self=False)

@socketio.on("connect")
def connect():
    print("Connected")
    send("Client connected!")


@socketio.on("join")
def join(data):
    name = data['name']
    room = data['room']
    join_room(room)
    send(f"{name} has joined the room {room}", to=room, broadcast=True)

@socketio.on("leave")
def leave(data):
    room = data['room']
    name = data['name']
    if name == None:
        print("Host")
        send(f"Host has left the room {room}",to=room, broadcast=True)
        emit("close", to=room, broadcast=True, include_self=False)
    else:
        print(name)
        send(f"{name} has left the room {room}",to=room, broadcast=True)
    leave_room(room)
    



@socketio.on("question")
def send_question(data):
    room = data["room"]
    question = data["room"]
    send(question, to=room, broadcast=True)


@socketio.on("start")
def start(data):
    send("start", to=data["room"], broadcast=True, include_self=False)
    emit("start", to=data["room"], broadcast=True, include_self=False)


@socketio.on("close")
def close(data):
    send("close", to=data["room"], broadcast=True)