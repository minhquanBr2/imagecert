import requests

BASE_URL = 'http://104.154.115.168:8003/'

def getKeyCert(uid):
    url = BASE_URL + 'select/key_certi'
    response = requests.get(url)
    return response.json()

def insertKeyCerti(payload):
    url = BASE_URL + 'insert/key_certi'
    response = requests.post(url, json=payload)
    return response.json()
    
