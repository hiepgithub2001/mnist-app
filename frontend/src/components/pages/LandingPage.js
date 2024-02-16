import React from 'react'
import { Link } from 'react-router-dom'
import './pages.css'
import MnistJobModal from '../MnistJob/MnistJobModal'

function LandingPage() {
  return (
    <div>
      <h1>Mnist App</h1>
      <button
        className="scoreboard-button"
        onClick={() => window.location.href = '/score_board'}
      >
        <h3> Score Board </h3>
      </button>
      <MnistJobModal />
    </div>
  )
}

export default LandingPage
