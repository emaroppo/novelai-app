import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import StoryList from './pages/StoryList'; // Adjust the path as needed

function App() {
  const [creatingStory, setCreatingStory] = useState(false);
  const [newStoryTitle, setNewStoryTitle] = useState('');

  const handleCreateStory = () => {
    setCreatingStory(true);
  };

  const handleSubmitNewStory = () => {
    // Call API to create a new story with newStoryTitle
    // Then refresh the list of stories or navigate to the new story's page
    setCreatingStory(false);
    setNewStoryTitle('');
  };

  return (
    <div>
      <h1>Interactive Storytelling App</h1>
      <StoryList />
      {creatingStory ? (
        <div>
          <input
            type="text"
            value={newStoryTitle}
            onChange={(e) => setNewStoryTitle(e.target.value)}
            placeholder="Story Title"
          />
          <button onClick={handleSubmitNewStory}>Submit</button>
        </div>
      ) : (
        <button onClick={handleCreateStory}>Create New Story</button>
      )}
    </div>
  );
}

export default App;
