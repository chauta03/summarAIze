import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Login from './components/LoginPage';
import Signup from './components/SignUpPage';
import logo from './logo.svg';
import AppCard from './components/AppCard';
import './App.css';
import LiveTranscription from './pages/LiveTransciption';

function App() {
  return (
    <>
      <Router>
        <div className="app-container">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
        </div>
      </Router>
      <div className="App">
        <LiveTranscription />
      </div>
    </>
  );
}

export default App;
