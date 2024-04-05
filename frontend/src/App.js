import React, { useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Outlet } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Courses from './components/Courses';
import About from './components/About';
import Contact from './components/Contact';
import Welcome from './components/Welcome';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ProgressPage from './components/ProgressPage';
import StudyPage from './components/StudyPage';
import AccountPage from './components/AccountPage';
import VerifyEmail from './components/VerifyEmail'; // Ensure this is imported.

// Import all other necessary components and the PrivateRoute
import PrivateRoute from './components/PrivateRoute';


function App() {
  const getEduTokenBalance = async () => {
    try {
      const response = await fetch('YOUR_BACKEND_ENDPOINT');
      await response.json(); // Presumably updating state or context
    } catch (error) {
      console.error('Error fetching EduToken balance:', error);
    }
  };

  useEffect(() => {
    getEduTokenBalance();
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<>
            <Header />
            <div className="main-content"><Outlet /></div>
            <Footer />
          </>}>
            <Route index element={<Welcome />} />
            <Route path="Welcome" element={<Welcome />} />
            <Route path="Home" element={<Home />} />
            <Route path="courses" element={<Courses />} />
            <Route path="about" element={<About />} />
            <Route path="contact" element={<Contact />} />
            <Route path="Login" element={<Login />} />
            <Route path="Register" element={<Register />} />
          </Route>
          
          {/* Dedicated route structure for Dashboard to avoid displaying the main Header */}
                        {/* Protect the dashboard and its nested routes */}
          <Route element={<PrivateRoute />}>
            <Route path="dashboard" element={<Dashboard />}>
              <Route index element={<p>Select an option from the dashboard.</p>} />
              <Route path="progress" element={<ProgressPage />} />
              <Route path="study" element={<StudyPage />} />
              <Route path="account" element={<AccountPage />} />
            </Route>
          </Route>
            <Route path="/verify/:token" element={<VerifyEmail />} /> {/* This should be outside the dashboard route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
