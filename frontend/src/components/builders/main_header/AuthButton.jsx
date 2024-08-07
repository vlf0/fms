import React, { useState } from "react";
import { Nav, Button } from "react-bootstrap";
// import { useNavigate } from "react-router-dom";
import "../styles/MainHeaderStyles.css";


const AuthButton = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const navigate = useNavigate();

  const handleAuthButtonClick = () => {
    setIsAuthenticated(!isAuthenticated);
  };

  return (
    <Nav className="ms-auto">
      <Button
        onClick={handleAuthButtonClick}
        className={`auth-button ${isAuthenticated ? 'logout' : 'login'}`}
      >
        {isAuthenticated ? 'Logout' : 'Login'}
      </Button>
      <Button
        onClick={handleAuthButtonClick}
        className="auth-button-icon"
      >
        {isAuthenticated ? '🔓' : '🔑'}
      </Button>
    </Nav>
  );
};

export default AuthButton;
