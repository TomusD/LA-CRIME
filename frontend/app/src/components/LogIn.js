import React, { useState } from 'react';
import './auth.css';

const LogIn = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Handle form submission for logging in
  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://localhost:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password, }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        if (!response.ok) {
          return response.json().then((data) => {
            setErrorMessage(JSON.stringify(data));
          });
        }
      })
      .then((data) => {
        if (data) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            alert('Login successful!');
            window.location.href = '/home';
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        setErrorMessage('An error occurred. Please try again.');
      });
  };

  return (
    <div className="auth-form-container">
    <h1>LA-CRIME DB</h1>
      <h2>Log In</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Log In</button>
      </form>
    </div>
  );
};

export default LogIn;
