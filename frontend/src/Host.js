import "./Host.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faXmark, faPlus, faMinus } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { base_url, dev_base_url } from "./global";
import socketClient from "./socketClient";

function Host() {
  const navigate = useNavigate();
  const [maxPlayers, setMaxPlayers] = useState(5);
  const [roomCode, setRoomCode] = useState("");
  const [roomName, setRoomName] = useState("");
  const [err, setErr] = useState(null);

  // useEffect(() => {}, []);

  function generateCode() {
    var charCode = "";
    for (let i = 0; i < 4; i++) {
      charCode += String.fromCharCode(Math.round(Math.random() * 26) + 65);
    }
    setRoomCode(charCode);
  }

  function hostRoom() {
    if (roomName === "") setErr("Enter Room name");
    else if (roomCode === "") setErr("Enter Room Code or Click Generate");
    else {
      axios
        .post(dev_base_url + "/rooms/create", {
          room_name: roomName,
          room_code: roomCode,
          max_players: maxPlayers,
        })
        .then((res) => {
          if (res["data"]["status"]) {
            socketClient.connect();
            socketClient.emit("join", { name: roomName, room: roomCode });
            navigate("/quiz", { state: { room_code: roomCode, isHost: true } });
          }
        });
    }
  }
  return (
    <div className="main">
      <div className="close" onClick={() => navigate("/")}>
        <FontAwesomeIcon icon={faXmark} size="2xl" />
      </div>
      <div className="title">
        <h2>Host a Room</h2>
      </div>
      <div className="container">
        {<div className="error">{err}</div>}
        <input
          value={roomName}
          onFocus={() => setErr(null)}
          onChange={(ev) => {
            setRoomName(ev.target.value);
          }}
          type="text"
          placeholder="Enter Room name"
        ></input>
        <div>
          <input
            type="text"
            placeholder="Enter Room code"
            onFocus={() => setErr(null)}
            value={roomCode}
            onChange={(ev) => {
              setRoomCode(ev.target.value);
            }}
          ></input>
          <button onClick={() => generateCode()}>Generate</button>
        </div>
        <div className="max-players">
          <p>Max Players:</p>
          <div>
            <button
              onClick={() => {
                if (maxPlayers > 2) setMaxPlayers(maxPlayers - 1);
              }}
            >
              <FontAwesomeIcon icon={faMinus} size="lg" />
            </button>
            <p>{maxPlayers}</p>
            <button
              onClick={() => {
                setMaxPlayers(maxPlayers + 1);
              }}
            >
              <FontAwesomeIcon icon={faPlus} size="lg" />
            </button>
          </div>
        </div>
        <button
          className="host-btn"
          onClick={() => {
            hostRoom();
          }}
        >
          Host Room
        </button>
      </div>
    </div>
  );
}

export default Host;
