from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import base64
from utils.key import generate_ca_key_pair, load_ca_private_key
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

app = FastAPI()

class PublicKeyRequest(BaseModel):
    user_public_key: str

class VerifyRequest(BaseModel):
    user_public_key: str
    challenge_response: str

generate_ca_key_pair()
challenge = os.urandom(32)  # Generating a challenge for the demo purpose

@app.get("/")
async def index():
    return {"message": "CA Server is running."}

@app.post("/challenge")
async def challenge_endpoint(request: PublicKeyRequest):
    user_public_key_pem = request.user_public_key
    user_public_key = serialization.load_pem_public_key(
        user_public_key_pem.encode(),
        backend=default_backend()
    )
    
    challenge_base64 = base64.b64encode(challenge).decode('utf-8')
    
    response = {
        'challenge': challenge_base64
    }
    return response

@app.post("/verify")
async def verify_endpoint(request: VerifyRequest):
    user_public_key_pem = request.user_public_key
    challenge_response = base64.b64decode(request.challenge_response)
    
    user_public_key = serialization.load_pem_public_key(
        user_public_key_pem.encode(),
        backend=default_backend()
    )
    
    try:
        user_public_key.verify(
            challenge_response,
            challenge,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except:
        return {"error": "Verification failed."}, 400
    
    ca_private_key = load_ca_private_key()
    signature = ca_private_key.sign(
        user_public_key_pem.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    response = {
        'signature': base64.b64encode(signature).decode('utf-8')
    }
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
