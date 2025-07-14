import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <span className="logo">IMS Dashboard</span>
      <button onClick={handleLogout} className="logout-btn">Logout</button>
    </nav>
  );
}
