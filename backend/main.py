from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from classes.story.Story import Story
from classes.story.Paragraph import Paragraph
from bson import json_util
from classes.story.ParagraphFragment import ParagraphFragment
from bson import ObjectId
from bson.json_util import dumps
import json 
#CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from classes.novel_api import NovelAPI
#dereference DBRef
from classes.novel_api import NovelAPI
import pickle

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