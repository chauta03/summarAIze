import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Login from './components/LoginPage';
import Signup from './components/SignUpPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
        </div>
    </Router>
  );
}

export default App;
