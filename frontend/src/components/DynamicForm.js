// DynamicForm.js
import React, { useState } from 'react';
import { TextField, Button, FormControl, FormLabel } from '@mui/material';

const InputField = ({ fieldConfig, handleChange }) => {
  const { type, mandatory, title } = fieldConfig;

  switch (type) {
    case 'TextField':
      return (
        <TextField
          label={title}
          required={mandatory}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
      );
    case 'TextArea':
      return (
        <TextField
          label={title}
          required={mandatory}
          onChange={handleChange}
          fullWidth
          margin="normal"
          multiline
          rows={4}
        />
      );
    // Add more cases for different input types as needed
    default:
      return null;
  }
};

const DynamicForm = ({ fields, onSubmit }) => {
  const [formData, setFormData] = useState({});

  const handleChange = (name) => (event) => {
    setFormData({ ...formData, [name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map((fieldConfig, index) => (
        <FormControl key={index} fullWidth margin="normal">
          <FormLabel>{fieldConfig.title}</FormLabel>
          <InputField
            fieldConfig={fieldConfig}
            handleChange={handleChange(fieldConfig.name)}
          />
        </FormControl>
      ))}
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </form>
  );
};

export default DynamicForm;
