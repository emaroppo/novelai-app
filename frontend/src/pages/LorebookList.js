import withFetchHOC from "../components/hoc/withFetchHOC";
import GridComponent from "../components/GridComponent";
import fetchLorebooks from "../utils/fetchLorebooks"; // Import your fetch function

const newElementLink = "/lorebook/create"; // Your link to the create lorebook page

const LorebookList = withFetchHOC(
  GridComponent,
  fetchLorebooks,
  newElementLink,
);

export default LorebookList;
