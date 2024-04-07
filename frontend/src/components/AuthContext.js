import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

// Helper function to get CSRF token from cookies
function getCsrfToken() {
  let csrfToken = null;
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith('csrftoken=')) {
      csrfToken = cookie.substring('csrftoken='.length);
      break;
    }
  }
  return csrfToken;
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Login function that updates isAuthenticated state based on response
  const login = async (userCredentials) => {
    const csrfToken = getCsrfToken();
    try {
      const response = await fetch('http://localhost:8000/login_api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include', // Important for sending cookies over fetch
        body: JSON.stringify(userCredentials),
      });

      if (response.ok) {
        setIsAuthenticated(true);
      } else {
        console.error('Login failed');
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Login error:', error);
      setIsAuthenticated(false);
    }
  };

  // Logout function that updates isAuthenticated state
  const logout = async () => {
    const csrfToken = getCsrfToken();
    try {
      await fetch('http://localhost:8000/logout/', { //logout_view maybe
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include', // Important for sending cookies over fetch
      });
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  useEffect(() => {
    // Function to check the session's validity on initial load
    const checkSession = async () => {
      try {
        const response = await fetch('http://localhost:8000/check_session/', {
          credentials: 'include',  // Ensures cookies, like session IDs, are included with the request
        });
  
        if (response.ok) {
          const data = await response.json();
          setIsAuthenticated(data.isAuthenticated);
        } else {
          console.error('Session check failed:', response.status);
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error checking session:', error);
        setIsAuthenticated(false);
      }
    };
  
    checkSession();
  }, []);
  

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
