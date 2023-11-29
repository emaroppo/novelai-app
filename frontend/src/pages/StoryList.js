// SomePage.js
import withFetchHOC from '../components/hoc/withFetchHOC';
import GridComponent from '../components/GridComponent';
import fetchStories from '../utils/fetchStories'; // Import your fetch function

const newElementLink = "/story/create"; // Your link to the create story page

const StoryList = withFetchHOC(GridComponent, fetchStories, newElementLink);

export default StoryList;
