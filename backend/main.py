from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from classes.story.Story import Story
from classes.story.Paragraph import Paragraph
from bson import json_util
from classes.story.ParagraphFragment import ParagraphFragment
#CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from classes.novel_api import NovelAPI
#dereference DBRef

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

    print(story.__dict__)

    story_text = story.render_story(story.active_fragment)
    print(story_text)

    return story_text

@app.post("/stories/{story_id}/interact")
def interact_with_story(story_id: str, interaction: InteractModel, choice: UserChoice):
    # Retrieve the story from the database
    story = Story.from_db(story_id)

    #dereference the active fragment


    # Process the user's choice
    new_text = story.process_user_choice(choice, interaction.user_input, api)

    # Return the updated story with the new text
    return {"story": story, "new_text": new_text}
