import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar"; // Import NavBar component

import StoryView from "./pages/StoryView";
import StoryList from "./pages/StoryList";
import StoryCreate from "./pages/StoryCreate";

const rootElement = document.getElementById("root");

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<StoryList />} />
        <Route path="/story/:storyId" element={<StoryView />} />
        <Route path="/story/create" element={<StoryCreate />} />
      </Routes>
    </Router>
  </React.StrictMode>,
);
