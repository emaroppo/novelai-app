from anytree import NodeMixin
from classes.story.ParagraphFragment import ParagraphFragment, Base
from bson import DBRef, ObjectId

class Paragraph(NodeMixin, Base):
    collection = "paragraphs"

    from anytree import NodeMixin
from classes.story.ParagraphFragment import ParagraphFragment, Base
from bson import DBRef, ObjectId

class Paragraph(NodeMixin, Base):
    collection = "paragraphs"
    

    def serialize(self):
        fragment_ids = [fragment._id for fragment in self.fragments if fragment._id is not None]
        for fragment in self.fragments:
            if fragment._id is None:
                fragment.save_to_db()
                fragment_ids.append(fragment._id)
        fragments = [DBRef('paragraph_fragments', frag_id) for frag_id in fragment_ids]

        parent_paragraph = ObjectId(self.parent._id) if self.parent else None
        parent_fragment = DBRef('paragraph_fragments', self.parent_fragment._id) if self.parent_fragment else None

        return {
            '_id': self._id,
            'fragments': fragments,
            'parent': parent_paragraph,
            'parent_fragment': parent_fragment,
            'children': [ObjectId(child._id) for child in self.children],
            'active_fragment': DBRef('paragraph_fragments', self.active_fragment._id) if self.active_fragment else None
        }

    @classmethod
    def deserialize(cls, data):
        fragments = [Base.db.dereference(frag) for frag in data.get('fragments', [])]
        fragments = [ParagraphFragment.deserialize(frag) for frag in fragments]
        active_fragment = Base.db.dereference(data.get('active_fragment')) if data.get('active_fragment') else None
        active_fragment = ParagraphFragment.deserialize(active_fragment) if active_fragment else None
        parent_fragment = Base.db.dereference(data.get('parent_fragment')) if data.get('parent_fragment') else None
        parent_fragment = ParagraphFragment.deserialize(parent_fragment) if parent_fragment else None

        parent = None
        if data.get('parent'):
            parent = cls.load_from_db(Base.db, data.get('parent'))
        

        return cls(fragments=fragments, parent=parent, active_fragment=active_fragment, _id=data.get('_id'))


    def save_to_db(self):
        Base.db.paragraphs.update_one(
            {'_id': self._id},
            {'$set': self.serialize()},
            upsert=True
        )
        return self._id
        

    @classmethod
    def load_from_db(cls, db, _id):
        # Load a Paragraph from the database by its _id
        data = db.paragraphs.find_one({'_id': _id})
        return cls.deserialize(db, data) if data else None

    def __init__(self, fragments=list(), _id=None, parent=None, children=None, parent_fragment=None, first=False, active_fragment=None):
        super().__init__()
        
        self._id = _id if _id else ObjectId()
        self.parent = parent
        self.children = children if children else []
        self.active_fragment = active_fragment  # Track the active fragment
        self.parent_fragment = parent_fragment  # The 'parent' fragment of this paragraph

        if first:
            self.fragments = [ParagraphFragment(text=' ', paragraph_id=str(self._id))]
            self.active_fragment = self.fragments[0]

        else:
            self.fragments = fragments
        

    def generate(self, api):
        # Generate text using the active fragment
        new_text = self.active_fragment.generate(api)
        if type(new_text) is str:
            # Create a new fragment with the generated text and append to the current paragraph
            new_fragment = ParagraphFragment(text=new_text, paragraph_id=self._id, parent=self.active_fragment)
            self.fragments.append(new_fragment)
            self.active_fragment = new_fragment  # Update the active fragment

        elif type(new_text) is tuple:
            # Handle paragraph break: Create a new fragment for the first part of the text
            first_part_fragment = ParagraphFragment(text=new_text[0], paragraph_id=self._id, parent=self.active_fragment)
            self.fragments.append(first_part_fragment)
            self.active_fragment = first_part_fragment  # Update the active fragment

            # Create a new paragraph and a new fragment for the second part of the text
            new_paragraph = Paragraph(parent=self.parent, parent_fragment=self.active_fragment)  # Set the parent of the new paragraph
            second_part_fragment = ParagraphFragment(text=new_text[1], paragraph=new_paragraph, parent=self.active_fragment)
            new_paragraph.fragments.append(second_part_fragment)
            new_paragraph.active_fragment = second_part_fragment  # Set the active fragment for the new paragraph

        return new_paragraph if type(new_text) is tuple else None
