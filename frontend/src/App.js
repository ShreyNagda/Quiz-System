import "./App.css";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import socketClient from "./socketClient";

function App() {
  useEffect(() => {
    window.addEventListener("popstate", (e) => {
      window.history.go(1);
    });
    socketClient.connect();
  }, []);
  const navigate = useNavigate();
  return (
    <div className="main">
      <h2>Quiz System</h2>

      <div className="container">
        <input type="text" placeholder="Enter nickname"></input>
        <input type="text" placeholder="Enter room code"></input>
        <div className="btn-container">
          <button onClick={() => {}}>Join</button>
          <button onClick={() => navigate("/host")}>Host</button>
        </div>
      </div>
    </div>
  );
}

export default App;
