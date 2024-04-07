import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ensure this is the correct import path

const AccountPage = () => {
  const [userData, setUserData] = useState({
    email: '',
    name: '',
    surname: '',
    dob: '',
    confirmName: '',
    confirmSurname: '',
    isSubmitted: false,
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const authContext = useAuth(); // Using the whole context for consistency

  // Log the entire authContext for debugging purposes
  console.log('AuthContext:', authContext);

  useEffect(() => {
    // Redirect if not authenticated, using the whole context for checking
    if (!authContext.isAuthenticated) {
      navigate('/login');
    }
  }, [authContext, navigate]);

  useEffect(() => {
    if (authContext.isAuthenticated) {
      const fetchData = async () => {
        const response = await fetch('http://localhost:8000/get_user_details/', {
          method: 'GET',
          credentials: 'include',
        });

        if (response.status === 401 || response.status === 403) {
          setError('Session expired or unauthorized access. Redirecting to login.');
          setTimeout(() => navigate('/login'), 3000);
        } else if (response.ok) {
          const data = await response.json();
          setUserData(prevState => ({
            ...prevState,
            email: data.email,
            name: data.name,
            surname: data.surname,
            dob: data.dob,
          }));
          setSuccess('Account details loaded successfully.');
        } else {
          throw new Error(`Network response was not ok: ${response.statusText}`);
        }
      };

      fetchData().catch(error => {
        console.error('Failed to load account details:', error);
        setError(`Failed to load account details: ${error.message}`);
      });
    }
  }, [authContext.isAuthenticated, navigate]);

  const handleChange = (event) => {
    setUserData({ ...userData, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (userData.name.trim() !== userData.confirmName.trim() ||
        userData.surname.trim() !== userData.confirmSurname.trim()) {
      setError('Name or surname does not match confirmation.');
      return;
    }

    const csrfToken = document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1];

    fetch('http://localhost:8000/set_user_details/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include',
      body: JSON.stringify({
        email: userData.email,
        name: userData.name,
        surname: userData.surname,
        dob: userData.dob,
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('HTTP error, unable to update account details');
      }
      return response.json();
    })
    .then(data => {
      if (data.success) {
        setSuccess('Account details updated successfully.');
        setUserData({ ...userData, isSubmitted: true });
      } else {
        setError(data.error || 'Unknown error occurred.');
      }
    })
    .catch(error => {
      setError(error.message);
    });
  };

  return authContext.isAuthenticated ? (
    <div>
      <h2>My Account</h2>
      <p>Email: {userData.email}</p>
      {userData.isSubmitted ? (
        <>
          <p>Name: {userData.name}</p>
          <p>Surname: {userData.surname}</p>
          <p>Date of Birth: {userData.dob}</p>
        </>
      ) : (
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Name" value={userData.name} onChange={handleChange} required />
          <input type="text" name="surname" placeholder="Surname" value={userData.surname} onChange={handleChange} required />
          <input type="date" name="dob" placeholder="Date of Birth" value={userData.dob} onChange={handleChange} required />
          <input type="text" name="confirmName" placeholder="Confirm Name" value={userData.confirmName} onChange={handleChange} required />
          <input type="text" name="confirmSurname" placeholder="Confirm Surname" value={userData.confirmSurname} onChange={handleChange} required />
          <button type="submit">Update Details</button>
          {error && <p className="error">{error}</p>}
          {success && <p className="success">{success}</p>}
        </form>
      )}
    </div>
  ) : null; // Only render if authenticated, similar to ProgressPage
};

export default AccountPage;
