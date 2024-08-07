import React, { useState } from 'react';
import RegistrationForm from './forms/RegistrationForm';
import LoginForm from './forms/LoginForm';


const AuthPage = () => {
  const [currentForm, setCurrentForm] = useState('login');

  const handleSwitchForm = (form) => {
    setCurrentForm(form);
  };

  return (
    <div className="auth-page">
      {currentForm === 'register' ? (
        <RegistrationForm onSwitchForm={handleSwitchForm} />
      ) : (
        <LoginForm onSwitchForm={handleSwitchForm} />
      )}
    </div>
  );
};

export default AuthPage;
