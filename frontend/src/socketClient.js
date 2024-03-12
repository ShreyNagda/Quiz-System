import { io } from "socket.io-client";
// const url = "https://quiz-system-zeta.vercel.app/";
const socketClient = io("http://127.0.0.1:5000/", {
  autoConnect: false,
  //   reconnection: true,
});

socketClient.on("message", (data) => {
  console.log(data);
});

export default socketClient;
