import React, { useState } from 'react';
import '../styles/auth_styles.css';


const LoginForm = ({ onSwitchForm }) => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const result = await response.json();

      const token = result.token;  // Get token from response
      console.log(response)
      console.log(result)
      console.log(token)

      const expires = new Date();
      expires.setHours(expires.getHours() + 1);
      document.cookie = `token=${token}; path=/; secure; samesite=strict`; // Set token into coockie

      setSuccess('Login successful!');
    } catch (error) {
      setError(error.message);
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
