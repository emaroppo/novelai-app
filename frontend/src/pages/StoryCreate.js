// CreateStoryPage.js
import React from "react";
import DynamicForm from "../components/DynamicForm";

const formFields = [
  {
    name: "title",
    title: "Title",
    type: "TextField",
    mandatory: true,
  },
  {
    name: "description",
    title: "Description",
    type: "TextArea",
    mandatory: false,
  },
];

/**
 * Submits a new story to the server.
 *
 * @param {Object} storyData - The data for the new story.
 * @return {Promise<Object>} A promise that resolves to the response from the server.
 */
async function submitStory(storyData) {
  const response = await fetch("http://localhost:8000/stories/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(storyData),
  });
  return response.json(); // Assuming the endpoint returns JSON
}

const StoryCreate = () => {
  const handleFormSubmit = async (formData) => {
    try {
      const storyId = await submitStory(formData);
      console.log("Story Created with ID:", storyId);
      // Redirect or handle success
    } catch (error) {
      console.error("Failed to create story:", error);
      // Handle error
    }
  };

  return (
    <div>
      <h1>Create New Story</h1>
      <DynamicForm fields={formFields} onSubmit={handleFormSubmit} />
    </div>
  );
};

export default StoryCreate;
