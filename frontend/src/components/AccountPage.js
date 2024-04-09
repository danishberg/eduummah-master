import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';  // Assuming this context provides authentication status
import { retrieveUserDetails, setUserDetails } from './api';  // API utility functions

const AccountPage = () => {
  const [userDetails, setUserDetailsState] = useState({
    email: '',  // Assuming email is part of the user details but cannot be changed by the user
    name: '',
    surname: '',
    dob: '',  // Format YYYY-MM-DD
    detailsSet: false,
  });
  const navigate = useNavigate();
  const authContext = useAuth();

  useEffect(() => {
    if (!authContext.isAuthenticated) {
      navigate('/login');
    } else {
      retrieveUserDetails()
        .then(response => response.json())
        .then(data => {
          // Assuming the backend indicates the details are set through a 'detailsSet' flag
          if (data.detailsSet) {
            setUserDetailsState({
              ...data,
              detailsSet: true,
            });
          }
        })
        .catch(error => {
          console.error('Error fetching user details:', error);
        });
    }
  }, [authContext, navigate]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setUserDetailsState(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!userDetails.detailsSet) {
      setUserDetails(userDetails)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            setUserDetailsState(prevState => ({
              ...prevState,
              detailsSet: true,
            }));
            // Optionally, update authContext if it should be aware of the details being set
            if (authContext.setUserDetailsSet) {
              authContext.setUserDetailsSet(true);
            }
          } else {
            alert('Error updating details. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error setting account details:', error);
        });
    }
  };

  return (
    <div>
      <h2>{userDetails.detailsSet ? 'Your Account Details' : 'Set Your Account Details'}</h2>
      {userDetails.detailsSet ? (
        <div>
          <p>Email: {userDetails.email}</p>
          <p>Name: {userDetails.name}</p>
          <p>Surname: {userDetails.surname}</p>
          <p>Date of Birth: {userDetails.dob}</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input type="text" name="name" value={userDetails.name} onChange={handleChange} required />
          </label>
          <br />
          <label>
            Surname:
            <input type="text" name="surname" value={userDetails.surname} onChange={handleChange} required />
          </label>
          <br />
          <label>
            Date of Birth:
            <input type="date" name="dob" value={userDetails.dob} onChange={handleChange} required />
          </label>
          <br />
          <button type="submit" disabled={userDetails.detailsSet}>Submit</button>
        </form>
      )}
    </div>
  );
};

export default AccountPage;
