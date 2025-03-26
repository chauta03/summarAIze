import React from 'react';
import './App.css'
import NavBar from './components/NavBar/NavBar'
import Dashboard from './components/Dashboard/Dashboard'
import BlenderModelViewer from './components/Blender/BlenderModelViewer';
import Stars from './components/Stars/Stars'

function App() {
  return (
    <div >
      <NavBar />
      <div className="earth-wrapper">
        <Stars />
        <BlenderModelViewer />
      </div>
      <Dashboard />
    </div>
  )
}

export default App