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
    name: "entries",
    title: "Entries",
    type: "ResultSelect",
    mandatory: false,
  },
];

/**
 * Submits a new lorebook to the server.
 *
 * @param {Object} lorebookData - The data for the new story.
 * @return {Promise<Object>} A promise that resolves to the response from the server.
 */
async function submitLorebook(lorebookData) {
  const response = await fetch("http://localhost:8000/lorebooks/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(lorebookData),
  });
  return response.json(); // Assuming the endpoint returns JSON
}

/**
 *
 * @return {React.Component} The lorebook creation page.
 */
const LorebookCreate = () => {
  const handleFormSubmit = async (formData) => {
    try {
      // formData should have the structure { title: 'lorebook_title', entries: ['entry_id1', 'entry_id2', ...] }
      const lorebookData = {
        title: formData.title, // This will grab the lorebook title from the TextField input
        entries: formData.entries || [], // Ensure it's an array, even if no entries are selected
      };

      const lorebookId = await submitLorebook(lorebookData);
      console.log("Lorebook Created with ID:", lorebookId);
      // Redirect or handle success
    } catch (error) {
      console.error("Failed to create lorebook:", error);
      // Handle error
    }
  };

  return (
    <div>
      <h1>Create New Lorebook</h1>
      <DynamicForm fields={formFields} onSubmit={handleFormSubmit} />
    </div>
  );
};

export default LorebookCreate;
