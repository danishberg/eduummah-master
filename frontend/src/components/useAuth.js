import { useContext } from 'react';
import AuthContext from './Login'; // Import AuthContext from Login.js

const useAuth = () => {
  return useContext(AuthContext);
};

export default useAuth;
