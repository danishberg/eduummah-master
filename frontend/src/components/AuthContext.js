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
  const [sessionKey, setSessionKey] = useState(localStorage.getItem('sessionKey') || null);
  const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail') || '');

  // Login function that updates isAuthenticated state and stores session key
  const login = async (userCredentials) => {
    const csrfToken = getCsrfToken();
    try {
      const response = await fetch('http://localhost:8000/login_api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(userCredentials),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('sessionKey', data.sessionKey); // Store session key in local storage
        localStorage.setItem('userEmail', data.email);
        setSessionKey(data.sessionKey);
        setUserEmail(data.email);  // Update userEmail state
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

  // Logout function that clears session key and updates isAuthenticated state
  const logout = async () => {
    const csrfToken = getCsrfToken();
    try {
      await fetch('http://localhost:8000/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
      });
      localStorage.removeItem('sessionKey');
      localStorage.removeItem('userEmail');  // Clear user email from local storage
      setSessionKey(null);
      setUserEmail('');  // Reset userEmail state
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  
  useEffect(() => {
    const checkSession = async () => {
      const sessionKey = localStorage.getItem('sessionKey');
      if (!sessionKey) {
        setIsAuthenticated(false);
        return;
      }
      
      try {
        const response = await fetch('http://localhost:8000/check_session/', {
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          setIsAuthenticated(data.isAuthenticated);
          if (!data.isAuthenticated) {
            localStorage.removeItem('sessionKey');
            localStorage.removeItem('userEmail');
            setSessionKey(null);
            setUserEmail('');
          }
        } else {
          console.error('Session check failed:', response.status);
          setIsAuthenticated(false);
          localStorage.removeItem('sessionKey');
          localStorage.removeItem('userEmail');
          setSessionKey(null);
          setUserEmail('');
        }
      } catch (error) {
        console.error('Error checking session:', error);
        setIsAuthenticated(false);
        localStorage.removeItem('sessionKey');
        localStorage.removeItem('userEmail');
        setSessionKey(null);
        setUserEmail('');
      }
    };

    checkSession();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, sessionKey, userEmail, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);