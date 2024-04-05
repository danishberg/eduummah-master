import { createContext, useState, useContext } from 'react';

const AuthContext = createContext(null);

// Define the getCookie function to retrieve a cookie value by name
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
    const csrfToken = getCookie('csrftoken');  // Use getCookie to retrieve CSRF token

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
        // Handle login failure as needed
      }
    } catch (error) {
      console.error('Login error:', error);
      // Handle exception
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    // Implement logout logic here
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
