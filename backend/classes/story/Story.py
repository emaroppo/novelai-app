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
        active_fragment = None
        if data.get("active_fragment"):
            active_fragment_data = Base.db.dereference(data.get("active_fragment"))
            active_fragment = ParagraphFragment.deserialize(active_fragment_data)

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
            self._id = Base.db.stories.insert_one(entry).inserted_id
        else:
            Base.db.stories.update_one({"_id": self._id}, {"$set": entry}, upsert=True)

    @classmethod
    def load_from_db(cls, _id):
        data = Base.db.stories.find_one({"_id": _id})
        return cls.deserialize(data) if data else None

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

    def render_story(self, target_fragment):
        # Initialize the story text
        story_text = ""

        # Check if the provided target_fragment is valid
        if not target_fragment or not isinstance(target_fragment, ParagraphFragment):
            return "Invalid fragment node."

        # Function to recursively build the story text
        def build_text(fragment):
            nonlocal story_text
            if fragment.parent:
                build_text(fragment.parent)
            story_text += fragment.text + "\n\n"

        # Start building the story text from the target fragment
        build_text(target_fragment)

        return story_text.strip()
    
    def add_user_input(self, fragment_id, input_text):
        # Find the paragraph fragment that precedes the user input
        preceding_fragment = ParagraphFragment.load_from_db(fragment_id)
        if not preceding_fragment:
            return "Invalid fragment ObjectId."

        # Create a new fragment with the user input
        new_fragment = ParagraphFragment(text=input_text, paragraph_id=preceding_fragment.paragraph_id, parent=preceding_fragment)
        new_fragment.save_to_db()
        
        #search paragraphs for the paragraph that contains the preceding fragment
        for paragraph in self.paragraphs:
            print(preceding_fragment.paragraph_id)
            if paragraph._id == preceding_fragment.paragraph_id:
                #add the new fragment to the paragraph
                paragraph.fragments.append(new_fragment)
                #update the active fragment of the paragraph
                paragraph.active_fragment = new_fragment
                #update the active paragraph of the story
                


        # Update the active fragment of the story
        self.active_fragment = new_fragment

        self.save_to_db()

        return "User input processed successfully."
