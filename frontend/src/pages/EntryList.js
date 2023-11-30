import withFetchHOC from "../components/hoc/withFetchHOC";
import GridComponent from "../components/GridComponent";
import fetchEntries from "../utils/fetchEntries";

const newElementLink = "/entry/create";

const EntryList = withFetchHOC(GridComponent, fetchEntries, newElementLink);

export default EntryList;
