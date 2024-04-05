// src/components/PrivateRoute.js

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext'; // import useAuth from where it is defined

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth(); // Use the useAuth hook here
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to the /login page, but save the current location they were trying to go to
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default PrivateRoute;
