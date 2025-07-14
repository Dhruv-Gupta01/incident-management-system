import React, { useState } from 'react';
import API from '../api';
import { useNavigate } from 'react-router-dom';
import '../App.css';

export default function Login() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ username: '', password: '' });

  const handleChange = (e) =>
    setCredentials({ ...credentials, [e.target.name]: e.target.value });

  const handleLogin = async () => {
    try {
      const res = await API.post('/login/', credentials);
      localStorage.setItem('token', res.data.access);
      navigate('/dashboard');
    } catch (err) {
      alert('Login failed!');
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <input name="username" onChange={handleChange} placeholder="Username" />
      <input name="password" type="password" onChange={handleChange} placeholder="Password" />
      <button onClick={handleLogin}>Login</button>
      <p style={{ textAlign: 'center', marginTop: '1rem' }}>
        Don't have an account? <a href="/register">Register</a>
      </p>
    </div>
  );
}
