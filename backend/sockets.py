import requests
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from app import app

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(data, room):
    send(data, to=room, broadcast=True, include_self=Flase)

@socketio.on("join")
def join(data):
    name = data['name']
    room = data['room']
    # res = requests.request("POST", "http://127.0.0.1:5000/api/rooms/players", json={"room_code": room, "name": name})
    
    join_room(room)
    send(f"{name} has joined the room {room}", to=room, broadcast=True)

@socketio.on("leave")
def leave(data):
    room = data['room']
    name = data['name']
    leave_room(room)
    print("Leave room")
    send(f"{name} has left the room {room}",to=room, broadcast=True)