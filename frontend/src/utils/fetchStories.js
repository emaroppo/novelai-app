/**
 * Fetches stories from the server.
 *
 * @return {Promise<Array>} A promise that resolves to an array of stories. Each story is an object with `_id`, `title`, `thumbnail`, and `link` properties.
 */
async function fetchStories() {
  const response = await fetch("http://localhost:8000/stories");
  const data = await response.json();
  const stories = data.map((story) => ({
    _id: story._id,
    title: story.title,
    thumbnail: undefined,
    link: `/story/${story._id}`,
  }));

  return stories;
}

export default fetchStories;
