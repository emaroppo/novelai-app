import DynamicForm from "../components/DynamicForm";
import React from "react";

const formFields = [
  {
    type: "TextField",
    mandatory: true,
    title: "Title",
    name: "title",
  },
  {
    type: "TextArea",
    mandatory: true,
    title: "content",
    name: "content",
  },
];

const EntryCreate = () => {
  const handleFormSubmit = async (formData) => {
    try {
      const entryId = await submitEntry(formData);
      console.log("Entry Created with ID:", entryId);
      // Redirect or handle success
    } catch (error) {
      console.error("Failed to create entry:", error);
      // Handle error
    }
  };
  const submitEntry = async (entryData) => {
    const response = await fetch("http://localhost:8000/entries/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(entryData),
    });
    return response.json(); // Assuming the endpoint returns JSON
  };

  return (
    <div>
      <h1>Create New Entry</h1>
      <DynamicForm fields={formFields} onSubmit={handleFormSubmit} />
    </div>
  );
};
export default EntryCreate;
