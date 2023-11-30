from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from classes.story.Story import Story
from classes.lorebook.Lorebook import Lorebook
from classes.lorebook.LorebookEntry import LorebookEntry
from bson import json_util
from bson import ObjectId
from bson.json_util import dumps
import json 
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from classes.novel_api import NovelAPI

novel_api=NovelAPI()


class UserChoice(str, Enum):
    accept = "accept"
    decline = "decline"
    save = "save"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Update this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Assume the models Story, Paragraph, and ParagraphFragment are imported and set up for MongoDB

class StoryModel(BaseModel):
    title: str

class InteractModel(BaseModel):
    user_input: str

api = NovelAPI()
#print current working directory
import os
print(os.getcwd())

@app.get("/stories")
def get_stories():
    # Retrieve stories from the database
    stories = Story.retrieve_all()
    response = [{'_id': str(story['_id']), 'title': story['title']} for story in stories]
    
    return response

@app.post("/stories/create")
async def create_story(request: Request):
    # Create a new story in the database
    story_data= await request.json()
    story = Story(**story_data)
    story_id=story.save_to_db()
    story_id = story._id
    story_id = json_util.dumps(story_id)
    
    return story_id

@app.get("/stories/{story_id}")
def get_story(story_id: str):
    # Retrieve a specific story from the database
    story = Story.deserialize(Story.from_db(story_id))
    story_text = story.render_story(story.active_fragment)
    story=json.loads(dumps(story.serialize()))
    print(story['active_fragment'])

    return {
        "active_fragment": story['active_fragment']['$id']['$oid'],
        "text": story_text,
        "title": story['title'],
    }


@app.post('/update_story/{story_id}/{fragment_id}')
async def update_story(story_id: str, fragment_id: str, request: Request):
    # Extract user_input from the request body
    data = await request.json()
    user_input = data.get("user_input")

    if not user_input:
        raise HTTPException(status_code=400, detail="User input is required")

    # Retrieve the story data from the database
    story = Story.deserialize(Story.from_db(story_id))
    print(story.__dict__)

    # Call the add_user_input method of the Story object
    result = story.add_user_input(ObjectId(fragment_id), user_input)

    # Save changes to the database
    story.save_to_db()
    # Return the updated story content
    story_text = story.render_story(story.active_fragment)
    story=json.loads(dumps(story.serialize()))
    print(story['active_fragment'])

    return {
        "active_fragment": story['active_fragment']['$id']['$oid'],
        "text": story_text,
        "title": story['title'],
    }

@app.post('/generate/{story_id}')
async def generate(story_id: str):
    # Retrieve the story data from the database
    story = Story.deserialize(Story.from_db(story_id))
    print(story.__dict__)

    # Call the generate method of the Story object
    story.generate(api)

    # Save changes to the database
    story.save_to_db()
    # Return the updated story content
    story_text = story.render_story(story.active_fragment)
    story=json.loads(dumps(story.serialize()))

    return {
        "active_fragment": story['active_fragment']['$id']['$oid'],
        "text": story_text,
        "title": story['title'],
    }

@app.get('/lorebooks')
def get_lorebooks():
    # Retrieve lorebooks from the database
    lorebooks = Lorebook.retrieve_all()
    response = [{'_id': str(lorebook['_id']), 'title': lorebook['title']} for lorebook in lorebooks]
    
    return response

@app.post('/lorebooks/create')
async def create_lorebook(request: Request):
    # Create a new lorebook in the database
    lorebook_data= await request.json()
    entries = lorebook_data.get("entries")
    entries = [ObjectId(entry) for entry in entries]
    if entries:
        entries = [LorebookEntry.load_from_db(entry) for entry in entries]
    lorebook_data['entries'] = entries
    lorebook = Lorebook(**lorebook_data)
    lorebook_id=lorebook.save_to_db()
    lorebook_id = lorebook._id
    lorebook_id = json_util.dumps(lorebook_id)
    
    return lorebook_id

@app.get('/lorebooks/{lorebook_id}')
async def get_lorebook(lorebook_id: str):
    # Retrieve a specific lorebook from the database
    lorebook = Lorebook.deserialize(Lorebook.from_db(lorebook_id))
    lorebook=json.loads(dumps(lorebook.serialize()))
    return {
        "title": lorebook['title'],
        "entries": [entry['$id']['$oid'] for entry in lorebook['entries']],
    }

@app.post('/lorebooks/{lorebook_id}/add_entry')
async def add_entry(lorebook_id: str, request: Request):
    # Extract title and content from the request body
    data = await request.json()
    title = data.get("title")
    content = data.get("content")

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")

    # Retrieve the lorebook data from the database
    lorebook = Lorebook.deserialize(Lorebook.from_db(lorebook_id))

    # Create a new LorebookEntry object
    entry = LorebookEntry(title=title, content=content)

    # Add the entry to the lorebook
    lorebook.add_entry(entry)

    # Save changes to the database
    lorebook.save_to_db()

    # Return the updated lorebook content
    lorebook=json.loads(dumps(lorebook.serialize()))
    return {
        "title": lorebook['title'],
        "entries": [entry['$id']['$oid'] for entry in lorebook['entries']],
    }

@app.post('/entries/')
async def get_entries(request: Request):
    # Extract title and content from the request body
    data = await request.json()
    if 'lorebook_id' in data:
        lorebook_id = data.get("lorebook_id")
        lorebook = Lorebook.deserialize(Lorebook.from_db(lorebook_id))
        lorebook=json.loads(dumps(lorebook.serialize()))
        return {
            "title": lorebook['title'],
            "entries": [entry['$id']['$oid'] for entry in lorebook['entries']],
        }
    else:
        entries = LorebookEntry.retrieve_all()
        response = [{'_id': str(entry['_id']), 'title': entry['title']} for entry in entries]
        return response
    
@app.post('/entries/create')
async def create_entry(request: Request):
    # Create a new entry in the database
    entry_data= await request.json()
    entry = LorebookEntry(**entry_data)
    entry_id=entry.save_to_db()
    entry_id = entry._id
    entry_id = json_util.dumps(entry_id)
    
    return entry_id