import requests
import pickle

with open("api_key.pickle", "rb") as f:
    api_key = pickle.load(f)


class NovelAPI:
    def __init__(self, api_key=api_key):
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {api_key}"})
        session.headers.update({"Content-Type": "application/json"})
        self.session = session

    def generate(self, input, parameters):
        response = self.session.post(
            "https://api.novelai.net/ai/generate",
            json={"input": input, "parameters": parameters},
        )
        return response.content.decode("utf-8")
