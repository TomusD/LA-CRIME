import React, { useState } from 'react';
import './auth.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [password_confirm, setPasswordConfirm] = useState('');
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Handle form submission for registering
  const handleSubmit = (e) => {
    e.preventDefault();
    
    fetch('http://localhost:8000/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        username, 
        email, 
        password, 
        password_confirm: password_confirm , 
        first_name, last_name
      }),
    })
      .then((response) => {
        if (response.ok) {
          alert('Registration successful!');
          window.location.href = '/login';
        }
        if (!response.ok) {
          return response.json().then((data) => {
            setErrorMessage(JSON.stringify(data));
            console.log(data);
          });
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        setErrorMessage('An error occurred. Please try again.');
      });
  };

  return (
    <div className="auth-form-container">
      <h1>Register</h1>
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
          Email:
          <input
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
        <label>
        Confirm Password:
          <input
            type="password"
            name="password"
            value={password_confirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
          />
        </label>
        <br />
        <label>
        First name:
          <input
            type="text"
            name="first_name"
            value={first_name}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </label>
        <br />
        <label>
        Last name:
          <input
            type="text"
            name="last_name"
            value={last_name}
            onChange={(e) => setLastName(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
