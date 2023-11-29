import requests
import pickle
api_key = 'pst-AQVP9fc3pGkdP32cy84LfUdY1Dewkjg1UD0zjf3WT3xGkqgw2aZ8zCEAZ8qpwdY4'
#pickle api key for future use
with open('api_key.pickle', 'wb') as f:
    pickle.dump(api_key, f)

#use persisten session to keep cookies
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})
session.headers.update({'Content-Type': 'application/json'})

#make request to api.novelai.net/ai/generate
response = session.post('https://api.novelai.net/ai/generate', json={
    'input': 'Lucy went to visit',
    'parameters': {
        'model':'kayra-v1',
        'min_length': 50,
        'max_length': 100,
        'use_string': True,
    }
})

print(response.content.decode('utf-8'))