import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import App from './App';
import StoryView from './pages/StoryView'; // Component to interact with a story
import StoryList from './pages/StoryList';
import StoryCreate from './pages/StoryCreate';

const rootElement = document.getElementById('root');

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<StoryList />} />
        <Route path="/story/:storyId" element={<StoryView />} />
        <Route path="/story/create" element={<StoryCreate />} />
      </Routes>
    </Router>
  </React.StrictMode>,
);
