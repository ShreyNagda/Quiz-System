import { io } from "socket.io-client";

const socketClient = io("http://127.0.0.1:5000/", {
  autoConnect: false,
  //   reconnection: true,
});

socketClient.on("connect", () => {
  console.log("Connected");
});

export default socketClient;
