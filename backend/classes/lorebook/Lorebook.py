from classes.base import Base
from bson import ObjectId, DBRef
from classes.lorebook.LorebookEntry import LorebookEntry

class Lorebook(Base):
    collection = "lorebooks"
    def __init__(self, _id=None, title=None, entries=None):
        super().__init__(_id)
        self.title = title
        self.entries = entries if entries else []
    
    def serialize(self):
        #if self.entries is a list of 
        return {
            "_id": self._id if self._id else ObjectId(),
            "title": self.title,
            "entries": [DBRef("lorebook_entries", entry._id) for entry in self.entries]
        }
    
    @classmethod
    def deserialize(cls, data):
        entries = [LorebookEntry.deserialize(entry) for entry in data.get("entries", [])]
        return cls(
            title=data.get("title"),
            entries=entries,
            _id=data.get("_id")
        )
    
    def save_to_db(self):
        super().save(self.serialize())
        return self._id
    
    @classmethod
    def load_from_db(cls, _id):
        lorebook = super().from_db(_id)
        return cls.deserialize(lorebook) if lorebook else None
    
    def add_entry(self, entry):

        self.entries.append(entry)
        self.save_to_db()

