from app import app
from sockets import socketio

if __name__ == "__main__":
    app.run(port=5000, debug=True)