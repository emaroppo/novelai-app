from classes.story.Paragraph import Paragraph, Base
from classes.story.ParagraphFragment import ParagraphFragment
import datetime
from bson import DBRef


class Story(Base):
    collection = "stories"

    def __init__(
        self,
        title,
        description=None,
        author="user",
        date=datetime.datetime.now(),
        paragraphs=None,
        _id=None,
    ):
        super().__init__(_id)
        self.title = title
        self.description = description
        self.author = author
        self.date = date
        self.paragraphs = paragraphs if paragraphs else []

    def serialize(self):
        return {
            "_id": self._id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "date": self.date,
            "paragraphs": [paragraph.serialize() for paragraph in self.paragraphs],
            "active_fragment": DBRef("paragraph_fragments", self.active_fragment._id)
            if self.active_fragment
            else None,
        }

    @classmethod
    def deserialize(cls, data):
        paragraphs = [
            Paragraph.deserialize(para_data) for para_data in data.get("paragraphs", [])
        ]
        print(data.get("active_fragment"))
        print(Base.db.dereference(data.get("active_fragment")))
        active_fragment = ParagraphFragment.deserialize(
            Base.db.dereference(data.get("active_fragment"))
        )
        print(active_fragment)
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            author=data.get("author"),
            date=data.get("date"),
            paragraphs=paragraphs,
            _id=data.get("_id"),
            active_fragment=active_fragment,
        )

    def save_to_db(self):
        entry = self.serialize()
        if self._id is None:
            entry.pop("_id")
            self._id = self.db[self.collection].insert_one(entry).inserted_id
        else:
            self.db[self.collection].update_one(
                {"_id": self._id}, {"$set": entry}, upsert=True
            )

    @classmethod
    def load_from_db(cls, _id):
        # Load a Story from the database by its _id
        data = Base.db.stories.find_one({"_id": _id})
        return cls.deserialize(Base.db, data) if data else None

    def __init__(
        self,
        title,
        _id=None,
        description=None,
        author="user",
        active_fragment=None,
        date=datetime.datetime.now(),
        paragraphs=None,
        active_paragraph=None,
    ):
        self.title = title

        self.default_config = {
            "model": "kayra-v1",
            "min_length": 50,
            "max_length": 100,
            "use_string": True,
        }

        self.description = description
        self.author = author
        self.date = date
        self._id = _id
        if paragraphs:
            self.paragraphs = paragraphs
        else:
            self.paragraphs = [Paragraph(first=True)]
        self.active_paragraph = (
            active_paragraph if active_paragraph else self.paragraphs[0]
        )
        if active_fragment:
            self.active_fragment = active_fragment
        else:
            self.active_fragment = self.active_paragraph.active_fragment

    def generate(self, api):
        # Call the generate method of the active paragraph
        new_paragraph = self.active_paragraph.generate(api)

        if new_paragraph:
            # Append the new paragraph to the story's paragraph list
            self.paragraphs.append(new_paragraph)
            # Update the active paragraph to the new paragraph
            self.active_paragraph = new_paragraph

        # update active fragment
        self.active_fragment = self.active_paragraph.active_fragment

    def render_story(self, fragment_node):
        # Initialize the story text
        story_text = ""

        # Check if the provided fragment_node is valid
        if not fragment_node or not isinstance(fragment_node, ParagraphFragment):
            return "Invalid fragment node."

        # Traverse the story from the start to the fragment_node
        for paragraph in self.paragraphs:
            for frag in paragraph.fragments:
                story_text += frag.text + "\n\n"
                if frag == fragment_node:
                    # Stop when the target fragment is reached
                    return story_text.strip()

        # If the fragment_node is not found in the story, return the full story
        return story_text.strip()
