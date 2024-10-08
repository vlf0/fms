import React, { useState } from "react";
import "../styles/ServicesStyles.css";


const ParserService = () => {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const API_BASE_URL = process.env.REACT_APP_API_HOST;

  const handleSubmit = async () => {
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/run_parser`, {
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

      const resultData = await response.json();
      console.log("Result:", resultData);

      setSuccess("Parser operation successful!");
    
    } catch (error) {
      setError("You are not authorized! [" + error.message + "]");
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
