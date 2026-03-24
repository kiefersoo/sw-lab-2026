import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SignIn from "./SignIn";
import CreateUser from "./CreateUser";
import Projects from "./Projects";
import HardwareManager from "./HardwareManager";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignIn />} />
        <Route path="/create-user" element={<CreateUser />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/hardware/:projId" element={<HardwareManager />} />
      </Routes>
    </Router>
  );
}

export default App;