import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Adjust the path as necessary

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [csrfToken, setCsrfToken] = useState(''); // Declare setCsrfToken using useState
  const navigate = useNavigate();
  const { login } = useAuth(); // Utilize the login function from AuthContext

  useEffect(() => {
    // Suppose getCsrfToken function fetches token from the server and updates state
    const getCsrfToken = async () => {
      const response = await fetch('/get-csrf-token');
      const data = await response.json();
      setCsrfToken(data.csrfToken); // Set CSRF token using setCsrfToken
    };

    getCsrfToken();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const userCredentials = { email, password, csrfToken };
      await login(userCredentials);
      navigate('/dashboard');
    } catch (error) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default Login;
