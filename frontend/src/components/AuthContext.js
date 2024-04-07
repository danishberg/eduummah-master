import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

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

// Then use this function when making fetch calls
const csrfToken = getCsrfToken();


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = async (userCredentials) => {
    const csrfToken = getCookie('csrftoken');
    try {
      const response = await fetch('http://localhost:8000/login_api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(userCredentials),
        credentials: 'include',
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

  const logout = async () => {
    try {
      await fetch('http://localhost:8000/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // You get this from your cookies
        },
        credentials: 'include',
      });
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Check session validity on initial load
  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch('http://localhost:8000/check_session/', {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // You get this from your cookies
          },
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setIsAuthenticated(data.isAuthenticated);
        }
      } catch (error) {
        console.error('Error checking session:', error);
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
