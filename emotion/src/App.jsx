import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useState } from "react";
import "./App.css";
import Login from "./Login";
import Emotion from "./Emotion";

const App = () => {
  const [username, setUserName] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login username={username} setUserName={setUserName} />}></Route>
        <Route
          path="/emotion"
          element={<Emotion username={username} />}
        ></Route>
      </Routes>
    </Router>
  );
};

export default App;
