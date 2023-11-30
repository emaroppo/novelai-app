from anytree import NodeMixin
from bson import ObjectId
from classes.base import Base


class ParagraphFragment(Base, NodeMixin):
    collection = "paragraph_fragments"

    def __init__(
        self, text, paragraph_id=None, config=None, _id=None, parent=None, children=None
    ):
        super().__init__(_id)
        NodeMixin.__init__(self, parent=parent, children=children)
        self.text = text
        self.paragraph_id = paragraph_id
        self.config = config if config else {}

    def serialize(self):
        entry = {"_id": self._id, "text": self.text, "config": self.config}
        if self.children:
            entry["children"] = [ObjectId(child._id) for child in self.children]
        if self.parent:
            entry["parent"] = ObjectId(self.parent._id)

        return entry

    @classmethod
    def deserialize(cls, data):
        parent = None
        if data.get("parent"):
            parent = cls.load_from_db(Base.db, data.get("parent"))

        children = []
        for child_id in data.get("children", []):
            child = cls.load_from_db(Base.db, child_id)
            if child:
                children.append(child)

        return cls(
            text=data.get("text"),
            config=data.get("config"),
            _id=data.get("_id"),
            parent=parent,
            children=children,
        )

    def save_to_db(self):
        entry = self.serialize()
        if self._id is None:
            entry.pop("_id")
            self._id = Base.db.paragraph_fragments.insert_one(entry).inserted_id
        else:
            Base.db.paragraph_fragments.update_one(
                {"_id": self._id}, {"$set": entry}, upsert=True
            )

    @classmethod
    def load_from_db(cls, _id):
        data = Base.db.paragraph_fragments.find_one({"_id": _id})
        return cls.deserialize(data) if data else None

    def __init__(
        self,
        text=None,
        _id=None,
        config=None,
        paragraph=None,
        parent=None,
        children=None,
    ):
        Base.__init__(self)
        NodeMixin.__init__(self)

        self._id = _id
        self.config = config if config else dict()

        self.paragraph = paragraph
        self.parent = parent

        if children:
            self.children = children
        if not text:
            self.text = self.generate()
        else:
            self.text = text

    def assemble_prompt(self):
        prompt = ""
        current_node = self

        # Traverse from current node to the root, concatenating the texts
        while current_node is not None:
            if current_node.text:
                prompt = current_node.text + "\n" + prompt
            current_node = current_node.parent

        return prompt.strip()

    def generate(self, story, api):
        prompt = self.assemble_prompt()
        new_text = api.generate(prompt, self.config)

        # Check for paragraph breaks
        if "\n\n" in new_text:
            parts = new_text.split("\n\n", 1)

            return parts[0], parts[1]
        else:
            return new_text
