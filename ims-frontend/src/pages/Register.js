import React, { useState } from 'react';
import API from '../api';
import { useNavigate } from 'react-router-dom';
import '../App.css';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '', email: '', password: '',
    phone: '', address: '', pin_code: '',
    city: '', country: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    const user = {
      username: form.username,
      email: form.email,
      password: form.password,
    };
    const profile = {
      phone: form.phone,
      address: form.address,
      pin_code: form.pin_code,
      city: form.city,
      country: form.country,
    };

    try {
      await API.post('/register/', { user, profile });
      alert('Registered successfully!');
      navigate('/');
    } catch (err) {
      alert('Registration failed!');
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>
      <input name="username" onChange={handleChange} placeholder="Username" />
      <input name="email" onChange={handleChange} placeholder="Email" />
      <input name="password" type="password" onChange={handleChange} placeholder="Password" />
      <input name="phone" onChange={handleChange} placeholder="Phone" />
      <input name="address" onChange={handleChange} placeholder="Address" />
      <input name="pin_code" onChange={handleChange} placeholder="Pin Code" />
      <input name="city" onChange={handleChange} placeholder="City" />
      <input name="country" onChange={handleChange} placeholder="Country" />
      <button onClick={handleRegister}>Register</button>
      <p style={{ textAlign: 'center', marginTop: '1rem' }}>
        Already have an account? <a href="/">Login</a>
      </p>
    </div>
  );
}
