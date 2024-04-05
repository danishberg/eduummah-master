import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate for redirection
import logo from '../logo.png'; // Adjust the path as necessary
import '../css/Header.css';

const DashboardHeader = () => {
  const navigate = useNavigate();

  const handleLogOff = (event) => {
    event.preventDefault(); // Prevent default link behavior

    // Here, you would clear the user's authentication details.
    // For example, if you're using localStorage to store a token:
    localStorage.removeItem('authToken');

    // If using context, you would reset the authentication state there.
    // Example: setAuthenticated(false);

    // Redirect to the login page or wherever is appropriate after log-off.
    navigate('/login');

    // If you have a logout API endpoint, you should call it here as well.
  };

  return (
    <header className="header">
      <div className="logo">
        <Link to="/dashboard">
          <img src={logo} alt="EduUmmah Logo" className="logo-image" />
        </Link>
        <Link to="/dashboard" className="logo-text">Dashboard</Link>
      </div>
      <nav className="nav">
        <ul className="nav-menu">
          <li><Link to="/dashboard/progress">Progress</Link></li>
          <li><Link to="/dashboard/study">Study</Link></li>
          <li><Link to="/dashboard/account">Account</Link></li>
          <li>
            {/* Update to call handleLogOff when clicked */}
            <a href="/login" onClick={handleLogOff}>Log Off</a>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default DashboardHeader;
