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

const Layout = () => {
  const location = useLocation();
  const showHeaderFooter = !location.pathname.startsWith('/dashboard');

  return (
    <div className="App">
      {showHeaderFooter && <Header />}
      <div className="main-content center">
        <Outlet />
      </div>
      {showHeaderFooter && <Footer />}
    </div>
  );
};

// Updated App component
function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            {/* Public Routes */}
            <Route index element={<Welcome />} />
            <Route path="welcome" element={<Welcome />} />
            <Route path="home" element={<Home />} />
            <Route path="courses" element={<Courses />} />
            <Route path="about" element={<About />} />
            <Route path="contact" element={<Contact />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="verify/:token" element={<VerifyEmail />} />

            {/* Nested Dashboard Routes inside Layout to inherit centering */}
            <Route path="dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>}>
              <Route index element={<p>Select an option from the dashboard.</p>} />
              <Route path="progress" element={<ProgressPage />} />
              <Route path="study" element={<StudyPage />} />
              <Route path="account" element={<AccountPage />} />
            </Route>
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
