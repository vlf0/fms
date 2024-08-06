import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
// import AuthPage from "./components/auth/AuthPage";
import MainPage from "./components/MainPage1";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        {/* <Route path="/main" element={<MainPage />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
