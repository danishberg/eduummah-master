// Header.js
import React from 'react';
import '../css/Header.css';
import logo from '../logo.png'; // Import the logo image

function Header() {
  return (
    <header className="header">
      <div className="logo">
        {/* Use the imported logo variable in the src attribute */}
        <img src={logo} alt="EduUmmah Logo" />
        <a href="/Welcome" className="logo-text">EduUmmah</a>
      </div>
      <nav className="nav">
        <ul className="nav-menu">
          {/* Use regular anchor tags for navigation */}
          <li><a href="/Home">Home</a></li>
          <li><a href="/courses">Courses</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
          {/* Add more menu items as needed */}
        </ul>
      </nav>
      <div className="auth">
        {/* Use regular anchor tags for authentication links */}
        <a href="/login" className="auth-link">Login</a>
        <a href="/register" className="auth-link">Register</a>
      </div>
    </header>
  );
}

export default Header;
