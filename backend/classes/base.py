import pymongo
from bson import ObjectId

class Base:
    
    db = pymongo.MongoClient('mongodb://localhost:27017').novelai
    collection = None

    @classmethod
    def from_db(cls, _id):
        print(_id)
        if type(_id) is str:
            _id = ObjectId(_id)
        entry = cls.db[cls.collection].find_one({"_id": _id})
        return entry
    
    @classmethod
    def retrieve_all(cls):
        return list(cls.db[cls.collection].find({}))
    
    def __init__(self, _id=None):
        self._id = _id
      
    def save(self, entry=None):
        
        if entry is None:
            entry = self.__dict__

        # If _id is None, create a new entry, else update existing entry
        if self._id is None:
            self._id = self.db[self.collection].insert_one(entry).inserted_id
        else:
            self.db[self.collection].update_one({"_id": self._id}, {"$set": entry}, upsert=True)


    def delete(self):
        # If _id is None, raise error
        if self._id is None:
            raise ValueError("Cannot delete object with no _id")
        
        # Delete object from database
        self.db[self.collection].delete_one({"_id": self._id})
        
        # Set _id to None
        self._id = None
    