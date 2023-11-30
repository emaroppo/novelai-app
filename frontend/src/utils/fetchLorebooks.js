/**
 * Fetches all lorebooks from the backend
 */
async function fetchLorebooks() {
  const response = await fetch("http://localhost:8000/lorebooks");
  const data = await response.json();
  const lorebooks = data.map((lorebook) => ({
    _id: lorebook._id,
    title: lorebook.title,
    thumbnail: undefined,
    link: `/lorebook/${lorebook._id}`,
  }));

  return lorebooks;
}

export default fetchLorebooks;
