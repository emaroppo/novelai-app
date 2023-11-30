from classes.base import Base
import datetime
from bson import ObjectId

default_config = {
            "model": "kayra-v1",
            "min_length": 50,
            "max_length": 100,
            "use_string": True,
        }

class LorebookEntry(Base):
    collection = "lorebook_entries"

    def __init__(self, title, content=None, _id=None, activation_keywords=None):
        super().__init__(_id)
        self.title = title
        self.content = content
        self.date = datetime.datetime.now()
        self.activation_keywords = activation_keywords if activation_keywords else []

    def serialize(self):
        return {
            "_id": self._id if self._id else ObjectId(),
            "title": self.title,
            "content": self.content,
            "date": self.date,
            "activation_keywords": self.activation_keywords,
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            title=data.get("title"),
            content=data.get("content"),
            _id=data.get("_id"),
            activation_keywords=data.get("activation_keywords"),
        )
    
    def save_to_db(self):
        super().save(self.serialize())
        return self._id
    
    @classmethod
    def load_from_db(cls, _id):
        entry = super().from_db(_id)
        return cls.deserialize(entry) if entry else None
    
    def generate(self, api, config=default_config):
        prompt = self.title + "\n\n" + self.content
        response = api.generate(prompt, config)
        #update content
        self.content += response['output']
        self.save_to_db()

    def add_activation_keyword(self, keyword):
        self.activation_keywords.append(keyword)
        self.save_to_db()
        
