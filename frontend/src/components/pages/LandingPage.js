import React, { useState } from 'react';
import './pages.css'
import MnistJobModal from '../MnistJob/MnistJobModal';
import ScoreBoardModal from '../MnistJob/ScoreBoardModal';
import JobDetailModal from '../MnistJob/JobDetailModal';

function LandingPage() {
  const [activeTab, setActiveTab] = useState('create_job');

  return (
    <div>
      <h1> Mnist Training Application </h1>
      <div className="tab-bar">
        <button
          onClick={() => setActiveTab('create_job')}
          className={activeTab === 'create_job' ? 'active' : ''}
        >
          Create Job
        </button>
        <button
          onClick={() => setActiveTab('job_detail')}
          className={activeTab === 'job_detail' ? 'active' : ''}>
          Job Details
        </button>
        <button
          onClick={() => setActiveTab('score_board')}
          className={activeTab === 'score_board' ? 'active' : ''}>
          Score Board
        </button>
      </div>

      {activeTab === 'create_job' && (
        <MnistJobModal />
      )}
      {activeTab === 'job_detail' && (
        <JobDetailModal />
      )}
      {activeTab === 'score_board' && (
        <ScoreBoardModal />
      )}
    </div>
  );
}

export default LandingPage;