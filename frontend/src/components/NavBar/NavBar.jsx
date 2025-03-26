import React from 'react';
import './NavBar.css';

function NavBar() {
  return (
    <div className="navbar">
      <ul>
        <li><a href="#dashboard">dashboard</a></li>
        <li><a href="#transcription">real-time transcription</a></li>
        <li><a href="#profile">profile</a></li>
      </ul>
    </div>
  );
}

export default NavBar;
