import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/LoginPage';
import Signup from './components/SignUpPage';
import './App.css';
import LiveTranscription from './components/LiveTransciption';
import NavBar from './components/NavBar/NavBar';
import Dashboard from './components/Dashboard/Dashboard';
import BlenderModelViewer from './components/Blender/BlenderModelViewer';
import Stars from './components/Stars/Stars';
import Profile from './components/Profile';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true); // Update the login state
  };

  return (
    <Router>
      <div className="app-container">
        <Routes>
          {/* Pass handleLogin as a prop to Login */}
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/live-transcription" element={<LiveTranscription />} />


          {/* If logged in, render the live transcription page, otherwise, redirect to login */}
          <Route
            path="/main-dashboard"
            element={isLoggedIn ? (
              <div>
                <NavBar />
                <div className="earth-wrapper">
                  <Stars />
                  <BlenderModelViewer />
                </div>
                <Profile />
                <Dashboard />
                <LiveTranscription />
              </div>
            ) : (
              <Navigate to="/login" /> // Redirect to login if not logged in
            )}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
