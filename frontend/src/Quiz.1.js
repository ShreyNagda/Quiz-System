import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import socketClient from "./socketClient";
import axios from "axios";

export function Quiz() {
  const { state } = useLocation();
  const { room_code } = state;
  const [room, setRoom] = useState({});
  useEffect(() => {
    window.addEventListener("popstate", (e) => {
      window.history.go(1);
    });
    axios.get(`http://127.0.0.1:5000/api/room/${room_code}`).then((res) => {
      console.log(res);
      setRoom(res["data"]);
      console.log(room);
    });
    socketClient.on("message", (data) => {
      console.log(data);
    });
  }, []);

  return <div></div>;
}
