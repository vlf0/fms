import React, { useState } from "react";
import "../../styles/AuthStyles.css";


const RegistrationForm = ({ onSwitchForm }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError('');
    setSuccess('');

    try {
      const response = await fetch("http://localhost:8000/api/v1/register", {
        method: "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, name, password }),
      });
      if (!response.ok) {
        throw new Error("User with this email is already exists");
      }
      setSuccess("Registration successful!");
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="auth-registration-form">
      <h2>Registration</h2>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            autoComplete="username"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
        <button type="button" onClick={() => onSwitchForm('login')}>Switch to Login</button>
      </form>
    </div>
  );
};

export default RegistrationForm;
