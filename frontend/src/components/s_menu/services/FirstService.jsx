import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
import "../styles/ServicesStyles.css";


const ParserService = () => {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  // const navigate = useNavigate();

  const handleSubmit = async () => {
    setError('');
    setSuccess('');

    try {
      const response = await fetch("http://localhost:8000/api/v1/check_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Ensure cookies are sent with the request
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Parser operation failed");
      }

      const result = await response.json(); 
      setSuccess("Parser operation successful!");
      console.log(result);

      // navigate("/main");
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="one-service-container">  
      <button className="services-button" onClick={handleSubmit}>
        Run Parser
      </button>
      {success && <div className="success-message">{success}</div>}
      {error && <div className="error-message">{error}</div>}
      <span className="description-text">
        This service is a parser of HeadHunter.ru - vacancy aggregator.
      </span>
    </div>
  );
};

export default ParserService;
