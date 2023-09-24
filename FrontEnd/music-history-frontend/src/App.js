import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Timeline from "./Components/Timeline/Timeline";

function App() {
  return (
    <Router>
      <h1 className="main-title">Music History Time-line</h1>
      <Routes>
        <Route path="/" element={<Timeline />} />
      </Routes>
    </Router>
  );
}

export default App;
