import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

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

  // A utility function to get a cookie by name.
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

  // Extract CSRF token value correctly
const getCSRFToken = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken'))
    .split('=')[1];
};

  useEffect(() => {
    fetch('http://localhost:8000/get_user_details/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),  // Use getCookie to retrieve the CSRF token
      },
      credentials: 'include',
    })
    .then(response => {
      if (response.status === 401 || response.status === 403) {
        setError('Session expired or unauthorized access. Redirecting to login.');
        navigate('/login');  // Redirect to login page
      //   return null;  -  Prevent further processing in the promise chain | Stage 2 Do not forget to check again if works
      } else if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      return response.json();
    })
    
    .then(data => {
      if (data) {  // Check if data is not null
        setUserData(prevState => ({
          ...prevState,
          email: data.email,
          name: data.name,
          surname: data.surname,
          dob: data.dob,
        }));
        setSuccess('Account details loaded successfully.');
      }
    })
    .catch(error => {
      console.error('Failed to load account details:', error);
      setError(`Failed to load account details: ${error.message}`);
    });
  }, [navigate]);

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

    fetch('/set_user_details/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
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

  return (
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
  );
};

export default AccountPage;
