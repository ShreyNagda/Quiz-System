from flask import Flask,request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

from dotenv import load_dotenv
import os

import uuid

load_dotenv()

app = Flask(__name__)
app.config['SECRET'] = os.getenv("SECRET")
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
CORS(app, origins="http://localhost:3000")
client = PyMongo(app)
db = client.db
rooms_collection = db.rooms

@app.route("/api", methods=["GET"])
def api():
    return jsonify("Server running on port: 5000")

@app.route("/api/rooms/create", methods=["POST"])
def create_room():
    json = request.json
    room_code = json['room_code']
    room_name = json['room_name']
    max_players = json['max_players']
    if check_room(room_code) == False:
        room = {
            "room_code": room_code,
            "room_name": room_name,
            "max_players": max_players,
            "players": [],
            "questions": []
        }
        rooms_collection.insert_one(room)
        return jsonify({"status":True, "msg": f"Room {room_code} created successfully!"})
    else:
        return jsonify({"status":False, "msg": f"Room code {room_code} currently used!"})

#Adding players to the room based on room code
@app.route("/api/rooms/<room_code>/addplayer", methods=["POST"])
def addplayer(room_code):
    player_name = request.json["name"]
    player_id = uuid.uuid4()
    player_score = 0
    if check_room(room_code):
        playerlist = get_playerlist(room_code)
        print(playerlist)
        player = {
            "player_id": player_id,
            "player_name": player_name,
            "player_score": player_score
        }
        playerlist.append(player)
        rooms_collection.find_one_and_update({"room_code": room_code}, {'$set': {"players": playerlist}})
        return jsonify({"status":True, "msg": f"Player {player_id} added successfully!"})
    else:
        return jsonify({"status":False, "msg": f"Room code {room_code} does not exist!"})

#Adding questions to the room based on the room code
@app.route("/api/rooms/<room_code>/addquestions", methods=["POST"])
def addquestions(room_code):
    questions = request.json["questions"]
    if check_room(room_code):
        question_list = get_questions(room_code)
        for i in questions: 
            question_list.append(i)
        rooms_collection.find_one_and_update({"room_code": room_code}, {'$set': {"questions": question_list}})
        return jsonify({"status":True, "msg": "Questions added successfully!"})
    else:
        return jsonify({"status":False, "msg": f"Room code {room_code} does not exist!"})


#Check if room exists in the database
def check_room(room_code):
    if len(get_room(room_code)) > 0:
        return True
    else:
        return False

# Get room with the room code
def get_room(room_code):
    return list(rooms_collection.find({"room_code": room_code}))[0]

#Get players from the room
def get_playerlist(room_code):
    room = get_room(room_code)
    return room['players']

# Get questions from the room
def get_questions(room_code):
    room = get_room(room_code)
    return room["questions"]

