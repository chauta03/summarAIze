import React from 'react';
import './SignUpPage.css';
import myImage from '/Users/janhiong/Downloads/Summarizer/summarAIze/frontend/src/assets/SignUp.png';


const Signup = () => {
  const backgroundStyle = {
    backgroundImage: `url(${myImage})`,
    backgroundSize:'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: '100%',
    height: '100vh'
  };

  return (
    <div className="signup-page" style={backgroundStyle}>
        {/* Login box */}
        <div className="signup-box">
          <h2 className="signup-title">sign up</h2>
          
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

            <div className="input-group">
              <input
                id="confirm password"
                type="password"
                placeholder="confirm password"
                required
              />
            </div>

            <button type="submit" className="signup-button">
              sign up
            </button>
          </form>

        </div>

    </div>
  )
}

export default Signup;