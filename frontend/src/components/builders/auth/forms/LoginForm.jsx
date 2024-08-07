import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "./funcs/AuthService";
import "../../styles/AuthStyles.css";


const LoginForm = ({ onSwitchForm }) => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

  const result = await loginUser(name, password);
    if (result.success) {
      setSuccess(result.message);
      navigate("/");
    } else {
      setError(result.message);
    }
  };

  return (
    <div className="auth-login-form">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Login</button>
        <button type="button" onClick={() => onSwitchForm('register')}>Registration</button>
      </form>
    </div>
  );
};

export default LoginForm;
