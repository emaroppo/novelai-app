// StoryView.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Typography, TextField, Button, Paper } from '@mui/material';

const StoryView = () => {
  const [storyContent, setStoryContent] = useState('');
  const [userInput, setUserInput] = useState('');
  const { storyId } = useParams(); // This hooks into the URL parameter

  useEffect(() => {
    // Fetch the story data from the server
    const fetchStory = async () => {
      const response = await fetch(`http://localhost:8000/stories/${storyId}`);
      const data = await response.json();
      setStoryContent(data); // Assuming 'content' is a field in your story object
    };

    fetchStory();
  }, [storyId]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async () => {
    // Handle the submit action, for example sending the input back to the server
    console.log('User Input:', userInput);
    // Clear the input field after submit
    setUserInput('');
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {storyContent.title} {/* Display the story title */}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {storyContent} {/* Display the story content */}
        </Typography>
      </Paper>
      <TextField
        label="Your Input"
        variant="outlined"
        fullWidth
        value={userInput}
        onChange={handleInputChange}
        margin="normal"
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        style={{ margin: '20px 0' }}
      >
        Send
      </Button>
    </Container>
  );
};

export default StoryView;
