import React, { useState } from 'react';
import './LoginPage.css';
import googleLogo from '../assets/google-logo.png';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import LoginImg from '../assets/LogIn.png';
import axios from 'axios'; // Import axios for making API calls

const Login = ({ onLogin }) => {
  const navigate = useNavigate(); // Initialize navigate function
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const backgroundStyle = {
    backgroundImage: `url(${LoginImg})`,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: '100%',
    height: '100vh'
  };

  // Handle form submission (login logic)
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent the default form submission

    try {
      // Make the API call to log in
      const response = await axios.post('http://127.0.0.1:8000/users/sign_in', {
        email,
        password,
      }, { withCredentials: true }); // Include credentials (cookies) in the request

      // Call onLogin to update the isLoggedIn state in the parent component
      onLogin(); // Update isLoggedIn after login is successful

      // After login, navigate to the main dashboard or live transcription page
      navigate('/main-dashboard'); // Redirect to the live-transcription page or dashboard
    } catch (error) {
      // Handle errors, e.g., invalid credentials
      setError(error.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="login-page" style={backgroundStyle}>
      <div className="login-hi"></div>
      <div className="login-box">
        <h2 className="login-title">log in</h2>

        {/* Google login button */}
        <button className="google-button">
          <img src={googleLogo} alt="Google logo" className="google-icon" />
        </button>

        <span className="divider">or use your account</span>

        {/* Login form */}
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <input
              id="email"
              type="email"
              placeholder="email"
              value={email} // Bind the email input to state
              onChange={(e) => setEmail(e.target.value)} // Update state on change
              required
            />
          </div>

          <div className="input-group">
            <input
              id="password"
              type="password"
              placeholder="password"
              value={password} // Bind the password input to state
              onChange={(e) => setPassword(e.target.value)} // Update state on change
              required
            />
          </div>

          <button type="submit" className="login-button">
            log in
          </button>
        </form>

        {error && <div className="error">{error}</div>} {/* Display error message if any */}

        <div className="login-links">
          <a href="#forgot" className="forgot-link">
            forgot your password?
          </a>

          <Link to="/signup" className="signup-link">
            don't have an account? <span>sign up</span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
