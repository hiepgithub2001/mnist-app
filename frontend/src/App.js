import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './components/pages/LandingPage';
import './App.css';
import ScoreBoardModal from './components/MnistJob/ScoreBoardModal';


const Router = () => {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" exact element={<LandingPage />} />
        <Route path="/score_board" exact element={<ScoreBoardModal />} />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
