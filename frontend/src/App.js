import "./App.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import socketClient from "./socketClient";
import axios from "axios";
import { dev_base_url } from "./global";

function App() {
  const [name, setName] = useState("");
  const [room, setRoom] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    window.addEventListener("popstate", (e) => {
      window.history.go(1);
    });
    socketClient.on("connect", () => {
      console.log("Connected");
    });
    socketClient.on("message", (data) => {
      console.log(data);
    });
  }, []);

  function join_room() {
    if (name === "") {
      setErr("Enter nickname!");
    } else if (room === "") {
      setErr("Enter room code!");
    } else {
      socketClient.connect();
      axios
        .post(`${dev_base_url}/rooms/${room}/addplayer`, { player_name: name })
        .then((res) => {
          console.log(res);
        });
      socketClient.emit("join", { name: name, room: room });
      navigate("/quiz", { state: { room_code: room, isHost: false } });
    }
  }

  const navigate = useNavigate();
  return (
    <div className="main">
      <h2>Quiz System</h2>

      <div className="container">
        <div className="error">{err}</div>
        <input
          type="text"
          placeholder="Enter nickname"
          onChange={(ev) => setName(ev.target.value)}
        ></input>
        <input
          type="text"
          placeholder="Enter room code"
          onChange={(ev) => setRoom(ev.target.value)}
        ></input>
        <div className="btn-container">
          <button
            onClick={() => {
              join_room();
            }}
          >
            Join
          </button>
          <button onClick={() => navigate("/host")}>Host</button>
        </div>
      </div>
    </div>
  );
}

export default App;
