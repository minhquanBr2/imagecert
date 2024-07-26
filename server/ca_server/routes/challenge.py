from mytypes.HashGeneratorFactory import get_crypto_hash_algorithm
from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import sys 
sys.path.append('..')
import os
from middleware.encryptDecrypt import session_keys
from cryptography.hazmat.primitives import serialization, hashes
from utils.key import load_ca_private_key, load_ca_public_key
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
import json
from request.certiRequest import insertKeyCerti
from mytypes.KeyCertiGenerator import KeyCertiGenerator

router = APIRouter(
    prefix = '/zkp',
    tags = ['zkp'],
)

# Store for challenges associated with public keys
challenge_store = {}

crypto_hash_algo = get_crypto_hash_algorithm()
ca_private_key = load_ca_private_key()
key_cert_generator = KeyCertiGenerator(ca_private_key, crypto_hash_algo)


@router.post("/challenge")
async def challenge_endpoint(request: Request):
    data = request.state.decrypted_payload
    data = json.loads(data)
    user_uid = data.get("user_id")
    user_public_key_pem = data.get("user_public_key")
    public_key_der = base64.b64decode(user_public_key_pem)
    user_public_key = serialization.load_der_public_key(
        public_key_der,
        backend=default_backend()
    )
    # user_public_key = serialization.load_pem_public_key(
    #     user_public_key_pem.encode(),
    #     backend=default_backend()
    # )
    print('\nchallenge_endpoint', data, user_uid, user_public_key)
    
    if not user_uid or not user_public_key:
        raise HTTPException(status_code=422, detail="user_uid and user_public_key are required")
    
    if not session_keys.get(user_uid):
        return JSONResponse(content={"message": "Unauthorized. User not authenticated in any session. Please handshake first"}, status_code=403)
    # if not session_keys[user_uid]:
    #     return JSONResponse(content={"message": "Unauthorized. User not authenticated in any session. Please handshake first"}, status_code=403)

    challenge = os.urandom(32)  # Generate a random challenge
    print('challenge', challenge)
    challenge_base64 = base64.b64encode(challenge).decode('utf-8')
    print('challenge_base64', challenge_base64)
    challenge_store[user_uid] = challenge  # Store the challenge for later verification

    # Encrypt the challenge using the user's public key
    encrypted_challenge = user_public_key.encrypt(
        challenge,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=crypto_hash_algo),
            algorithm=crypto_hash_algo,
            label=None
        )
    )

    encrypted_challenge_base64 = base64.b64encode(encrypted_challenge).decode('utf-8')

    response = {
        'challenge': encrypted_challenge_base64
    }
    return response

@router.post("/verify")
async def verify_endpoint(request: Request):
    data = request.state.decrypted_payload
    data = json.loads(data)
    user_uid = data.get("user_id")
    user_public_key_pem = data.get("user_public_key")
    print('\nverify_endpoint', data, user_uid, user_public_key_pem)
    challenge_response = base64.b64decode(data.get("challenge_response"))

    if user_uid not in challenge_store:
        return JSONResponse(content={"message": "Challenge not found for the provided public key."}, status_code=400)
        
    challenge = challenge_store.pop(user_uid)  # Get the stored challenge
    
    if challenge_response != challenge:
        return JSONResponse(content={"message": "Verification failed. Challenge response does not match the challenge."}, status_code=400)
        
    # SIGN CERTI
    certi_payload = key_cert_generator.generate_key_certificate(user_uid, user_public_key_pem)
    certi_payload["user_uid"] = user_uid

    print('certi_payload', certi_payload)

    # Insert certificate into DB
    db_response = insertKeyCerti(certi_payload)
    print('status code', db_response.status_code)
    print('content', db_response.json())

    return JSONResponse(status_code=db_response.status_code, content=db_response.json())

