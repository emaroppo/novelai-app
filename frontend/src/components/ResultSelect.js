import React, { useState, useEffect } from "react";
import {
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  FormLabel,
  Button,
} from "@mui/material";
import fetchEntries from "../utils/fetchEntries";
import PropTypes from "prop-types";

const ResultSelect = ({ handleChange }) => {
  const [entries, setEntries] = useState([]);
  const [selectedEntries, setSelectedEntries] = useState([]);

  useEffect(() => {
    const getEntries = async () => {
      const fetchedEntries = await fetchEntries();
      setEntries(fetchedEntries);
    };

    getEntries();
  }, []);

  const handleSelect = (entry) => {
    const updatedSelection = selectedEntries.includes(entry._id)
      ? selectedEntries.filter((id) => id !== entry._id)
      : [...selectedEntries, entry._id];

    setSelectedEntries(updatedSelection);
    handleChange(updatedSelection); // handleChange now receives an array of entry IDs
  };

  if (entries.length === 0) {
    return (
      <Button href="/entry/create" variant="contained" color="primary">
        Create New Result
      </Button>
    );
  }

  return (
    <FormControl component="fieldset">
      <FormLabel component="legend">Select Results</FormLabel>
      <FormGroup>
        {entries.map((entry) => (
          <FormControlLabel
            key={entry._id}
            control={
              <Checkbox
                checked={selectedEntries.includes(entry._id)}
                onChange={() => handleSelect(entry)}
              />
            }
            label={entry.title}
          />
        ))}
      </FormGroup>
      <Button href="/entry/create" variant="contained" color="primary">
        Create New Result
      </Button>
    </FormControl>
  );
};
// Prop validation
ResultSelect.propTypes = {
  handleChange: PropTypes.func.isRequired,
};

export default ResultSelect;
