import requests
from config import DB_ENDPOINT_URL

def getKeyCert(uid):
    url = DB_ENDPOINT_URL + '/select/key_certi'
    response = requests.get(url)
    return response.json()

def insertKeyCerti(payload):
    url = DB_ENDPOINT_URL + '/insert/key_certi'
    response = requests.post(url, json=payload)
    return response
    
