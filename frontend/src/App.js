import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation, Outlet } from 'react-router-dom';
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
import VerifyEmail from './components/VerifyEmail';

import { AuthProvider } from './components/AuthContext';
import PrivateRoute from './components/PrivateRoute';

// Create a component that decides whether to show the header
const Layout = () => {
  const location = useLocation();

  // Do not show the main header on the dashboard and its child routes
  const showHeader = !location.pathname.startsWith('/dashboard');

  return (
    <div className="App"> {/* Add App class for centering */}
      {showHeader && <Header />}
      <div className="main-content center"> {/* Apply centering styles */}
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Welcome />} />
            <Route path="welcome" element={<Welcome />} />
            <Route path="home" element={<Home />} />
            <Route path="courses" element={<Courses />} />
            <Route path="about" element={<About />} />
            <Route path="contact" element={<Contact />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="verify/:token" element={<VerifyEmail />} />
            {/* Nested routes under "/" will use the Layout and hence have the Header and Footer */}
          </Route>

          {/* Dashboard route is outside the Layout, so it won't have the Header and Footer from Layout */}
          <Route path="dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>}>
            <Route index element={<p>Select an option from the dashboard.</p>} />
            <Route path="progress" element={<ProgressPage />} />
            <Route path="study" element={<StudyPage />} />
            <Route path="account" element={<AccountPage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
