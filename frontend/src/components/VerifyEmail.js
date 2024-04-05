import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const VerifyEmail = () => {
  const { token } = useParams();
  const [message, setMessage] = useState('Verifying your email...');
  const navigate = useNavigate();

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await fetch(`http://localhost:8000/verification/verify-email/${token}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });
  
        if (response.ok) {
          setMessage('Email verified successfully. You can now log in.');
          navigate('/login');
        } else {
          const error = await response.json();
          setMessage(error.error || 'Failed to verify email. Please contact support or try again.');
        }
      } catch (error) {
        setMessage('An error occurred. Please try again later.');
      }
    };
  
    verifyEmail();
  }, [token, navigate]);
  
  return (
    <div>
      <h2>Email Verification</h2>
      <p>{message}</p>
    </div>
  );
};

export default VerifyEmail;
