import React from 'react';
import './LoginPage.css';
import googleLogo from '../assets/google-logo.png';
import { Link } from 'react-router-dom';
import LoginImg from '../assets/LogIn.png';


const Login = () => {
  const backgroundStyle = {
    backgroundImage: `url(${LoginImg})`,
    backgroundSize:'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: '100%',
    height: '100vh'
  };

  return (
    <div className="login-page" style={backgroundStyle}>
        {/* Login box */}
        <div className="login-box">
          <h2 className="login-title">log in</h2>
          
          {/* Goole login buttion */}
          <button className="google-button">
            <img src={googleLogo} alt="Google logo" className="google-icon" />  
          </button>
          
          <span className="divider">or use your account</span>

          <form>
            <div className="input-group">
              <input
                id="email"
                type="email"
                placeholder="email"
                required
              />
            </div>

            <div className="input-group">
              <input
                id="password"
                type="password"
                placeholder="password"
                required
              />
            </div>

            <button type="submit" className="login-button">
              log in
            </button>
          </form>

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
  )
}

export default Login;