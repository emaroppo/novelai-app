import React from "react";
import {
  Card,
  CardActionArea,
  CardMedia,
  CardContent,
  Typography,
  Grid,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

const GridComponent = ({ data, newElementLink }) => {
  return (
    <Grid container spacing={2}>
      {data.map((item) => (
        <Grid item key={item._id} xs={12} sm={6} md={4} lg={3}>
          <Card>
            <CardActionArea component={Link} to={item.link}>
              <CardMedia
                component="img"
                height="140"
                image={item.thumbnail || "default-thumbnail.jpg"}
                alt={item.title}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  {item.title}
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
      ))}
      <Grid item xs={12} sm={6} md={4} lg={3}>
        <Button
          variant="contained"
          component={Link}
          to={newElementLink}
          fullWidth
        >
          Add New Element
        </Button>
      </Grid>
    </Grid>
  );
};

GridComponent.propTypes = {
  data: PropTypes.array.isRequired,
  newElementLink: PropTypes.string.isRequired,
};

export default GridComponent;
