from flask import Flask,request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

from dotenv import load_dotenv
import os

import uuid

load_dotenv()

app = Flask(__name__)
app.config['SECRET'] = os.getenv("SECRET")
# print(os.getenv('MONGODB_URI'), type(os.getenv('MONGODB_URI')))
MONGO_URI = os.getenv("MONGO_URI")
app.config['MONGO_URI'] = MONGO_URI
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
    if checkRoom(room_code) == False:
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
    if checkRoom(room_code):
        playerlist = getPlayerList(room_code)
        print(playerlist)
        player = {
            "player_id": str(player_id),
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
    if checkRoom(room_code):
        question_list = getQuestions(room_code)
        for i in questions: 
            question_list.append(i)
        rooms_collection.find_one_and_update({"room_code": room_code}, {'$set': {"questions": question_list}})
        return jsonify({"status":True, "msg": "Questions added successfully!"})
    else:
        return jsonify({"status":False, "msg": f"Room code {room_code} does not exist!"})

@app.route("/api/rooms/<room_code>/getplayers", methods=["GET"])
def get_players(room_code):
    return getPlayerList(room_code)


#Check answer and increment score
@app.route("/api/rooms/<room_code>/checkanswer", methods=["POST"])
def checkanswer(room_code):
    if checkRoom(room_code):
        player_id = request.json["player_id"]
        question_no = request.json["question_no"]
        answer = request.json["answer"]

        question = getQuestioByQuestionNumber(room_code, question_no)
        players  = getPlayerList(room_code)
        for player in players:
            if player["player_id"] == player_id: 
                if question["correct_option"] == answer:
                    player["player_score"] += 1
                    rooms_collection.find_one_and_update({"room_code": room_code}, {"$set": {"players": players}})
                    return jsonify("Correct Answer")
    else:
        return jsonify({"status":False, "msg": f"Room code {room_code} does not exist!"})


#Check if room exists in the database
def checkRoom(room_code):
    if len(getRoom(room_code)) > 0:
        return True
    else:
        return False


# Get room with the room code
def getRoom(room_code):
    return list(rooms_collection.find({"room_code": room_code}))

#Get players from the room
def getPlayerList(room_code):
    room = getRoom(room_code)[0]
    return room['players']

# Get questions from the room
def getQuestions(room_code):
    room = getRoom(room_code)[0]
    return room["questions"]

def getQuestioByQuestionNumber(room_code, question_no):
    questions = getQuestions(room_code)
    for i in questions:
        if i["question_no"] == question_no:
            return i