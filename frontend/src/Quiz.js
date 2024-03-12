import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import socketClient from "./socketClient";
import axios from "axios";
import { dev_base_url } from "./global";

function Quiz() {
  const navigate = useNavigate();

  const { state } = useLocation();
  const { room_code, isHost } = state;
  const [room, setRoom] = useState({});
  useEffect(() => {
    window.addEventListener("beforeunload", () => {
      socketClient.emit("leave", { room: room_code });
      setTimeout(() => {
        navigate("/");
      }, 1000);
    });

    window.addEventListener("popstate", (e) => {
      window.history.go(1);
    });
    axios.get(`${dev_base_url}/room/${room_code}`).then((res) => {
      res && setRoom(res.data);
    });
    socketClient.on("message", (data) => {
      console.log(data);
    });
  }, [room_code, navigate]);

  return (
    room && (
      <div>
        <div>{room["room_name"]}</div>
        <div>{room["room_code"]}</div>
        <div>{isHost}</div>
      </div>
    )
  );
}
export default Quiz;
