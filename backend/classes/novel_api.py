import requests
import pickle
import json

with open("api_key.pickle", "rb") as f:
    api_key = pickle.load(f)

print(api_key)

class NovelAPI:
    def __init__(self, api_key=api_key):
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {api_key}"})
        session.headers.update({"Content-Type": "application/json"})
        self.session = session

    def generate(self, input, parameters):
        #print headers
        print(self.session.headers)
        response = self.session.post(
            "https://api.novelai.net/ai/generate",
            json={"input": input, "parameters": parameters},
        )
        return json.loads(response.content.decode("utf-8"))['output']
