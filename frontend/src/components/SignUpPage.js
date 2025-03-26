import React, { useState } from 'react';
import './SignUpPage.css';
import SignUpImg from '../assets/SignUp.png';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const navigate = useNavigate();
  
  // Define state variables with consistent naming.
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName]   = useState('');
  const [email, setEmail]         = useState('');
  const [password, setPassword]   = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError]         = useState('');
  const [loading, setLoading]     = useState(false);

  const backgroundStyle = {
    backgroundImage: `url(${SignUpImg})`,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: '100%',
    height: '100vh'
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Check if the passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/users/sign_up', {
        first_name,
        last_name,
        email,
        password,
      });
    
      // Check if the response data has a message, and alert it
      alert(response?.data?.message || 'Sign up successful!');
      navigate('/login'); // Redirect to login page after successful sign-up
    } catch (err) {
      // Handle error properly
      const errorMessage = err?.response?.data?.message || 'Sign up failed';
      alert(errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page" style={backgroundStyle}>
      <div className="signup-box">
        <h2 className="signup-title">sign up</h2>

        <form onSubmit={handleSignUp}>
          <div className="input-group">
            <input
              type="text"
              placeholder="First Name"
              value={first_name}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <input
              type="text"
              placeholder="Last Name"
              value={last_name}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Confirm Password Field */}
          <div className="input-group">
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit" className="signup-button" disabled={loading}>
            {loading ? 'Signing Up...' : 'Sign Up'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
