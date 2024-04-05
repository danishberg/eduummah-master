import React, { useState, useEffect } from 'react';

const AccountPage = () => {
  const [userData, setUserData] = useState({
    name: '',
    surname: '',
    dob: '',
    confirmName: '',
    confirmSurname: '',
    isSubmitted: false,
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/get_user_details/', {
      method: 'GET',
      credentials: 'include',
    })
    .then(response => {
      if (response.redirected) {
        throw new Error('Session expired or user not logged in. Redirecting to login.');
      }
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data && data.email) {
        setUserData(prevState => ({
          ...prevState,
          email: data.email,  // Display email without editing capability
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
  }, []);

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
      },
      body: JSON.stringify({
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
      <p>Email: {userData.email}</p> {/* Display email without allowing edits */}
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
