import React, { useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';  // Import useAuth hook
import { useNavigate } from 'react-router-dom';  // Import useNavigate hook for redirection

const ProgressPage = () => {
  const authContext = useAuth(); // Consume the AuthContext
  const navigate = useNavigate();

  // Log the entire authContext for debugging purposes
  console.log('AuthContext:', authContext);

  useEffect(() => {
    // If isAuthenticated is false, redirect to a different page, e.g., login page
    if (!authContext.isAuthenticated) {
      navigate('/login'); // Redirect user to login if not authenticated
    }
  }, [authContext, navigate]);

  // Your component only renders if the user is authenticated
  return authContext.isAuthenticated ? (
    <div>
      <h2>My Progress</h2>
      <p>Progress details will be displayed here.</p>
    </div>
  ) : null;  // Or render a loading indicator until the authentication check is complete
};

export default ProgressPage;
