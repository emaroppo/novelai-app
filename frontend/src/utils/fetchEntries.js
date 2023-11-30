/**
 * retrieve entries from the backend
 */
async function fetchEntries() {
  const response = await fetch("http://localhost:8000/entries", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: {},
      projection: {
        title: 1,
      },
    }),
  });

  const data = await response.json();

  const entries = data.map((entry) => ({
    _id: entry._id,
    title: entry.title,
    thumbnail: undefined,
    link: `/entry/${entry._id}`,
  }));

  return entries;
}
export default fetchEntries;
