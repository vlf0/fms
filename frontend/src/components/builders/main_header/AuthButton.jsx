import React, { useState, useEffect } from "react";
import { Nav, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { checkAuth } from "../auth/forms/funcs/AuthService";
import "../styles/MainHeaderStyles.css";


const AuthButton = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const verifyAuth = async () => {
      const result = await checkAuth();
      setIsAuthenticated(result.success);
    };
    verifyAuth();
  }, []);
  
  const handleAuthButtonClick = async () => {

    if (isAuthenticated) {
      try {
        await fetch("http://159.65.135.38:80/api/v1/logout", {
          method: "POST",
          credentials: "include",
        });
        setIsAuthenticated(false);
      } catch (error) {
        console.error("Logout failed:", error);
      }
    } else {
      navigate("/login");
    }
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
