import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Typography, TextField, Button, Paper } from "@mui/material";

const StoryView = () => {
  const [storyContent, setStoryContent] = useState({
    title: "",
    text: "",
    active_fragment: "",
  });
  const [userInput, setUserInput] = useState("");
  const { storyId } = useParams(); // This hooks into the URL parameter

  useEffect(() => {
    // Fetch the story data from the server
    const fetchStory = async () => {
      const response = await fetch(`http://localhost:8000/stories/${storyId}`);
      const data = await response.json();
      setStoryContent(data);
    };

    fetchStory();
  }, [storyId]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async () => {
    const fragmentId = storyContent.active_fragment;
    console.log("Submitting:", userInput);

    try {
      const response = await fetch(
        `http://localhost:8000/update_story/${storyId}/${fragmentId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fragment_id: fragmentId,
            user_input: userInput,
          }),
        },
      );
      const updatedStory = await response.json();

      setStoryContent(updatedStory); // Update the displayed story with the new content
      setUserInput(""); // Clear the input field after submit
    } catch (error) {
      console.error("Error updating story:", error);
    }
  };
  const handleGenerateContent = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/generate/${storyId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // include other necessary headers
          },
          // include body if required
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const newStoryData = await response.json();
      setStoryContent(newStoryData); // Update your story state here
    } catch (error) {
      console.error("Error generating story:", error);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} style={{ padding: "20px", marginTop: "20px" }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {storyContent.title}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {storyContent.text}
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
        style={{ margin: "20px 10px 20px 0" }}
      >
        Send
      </Button>
      <Button
        variant="contained"
        color="secondary"
        onClick={handleGenerateContent}
        style={{ margin: "20px 0" }}
      >
        Generate
      </Button>
    </Container>
  );
};

export default StoryView;
