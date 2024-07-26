from mytypes.HashGeneratorFactory import get_crypto_hash_algorithm
from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import sys 
sys.path.append('..')
from mytypes.model import ClientHelloRequest, EncryptedPayloadRequest
import json
from middleware.encryptDecrypt import session_keys
from cryptography.hazmat.primitives import serialization, hashes
from utils.key import load_ca_private_key, load_ca_public_key
from cryptography.hazmat.primitives.asymmetric import padding
import base64

router = APIRouter(
    prefix = '/handshake',
    tags = ['handshake'],
)

crypto_hash_algo = get_crypto_hash_algorithm()

@router.post("/client_hello")
async def client_hello(request: ClientHelloRequest, auth_request: Request):
    if request.client_hello != 'Hello from Client':
        return JSONResponse(content={"message": "Invalid client hello message."}, status_code=400)

    if not auth_request.state.user:
        return JSONResponse(content={"message": "Unauthorized. User not authenticated."}, status_code=403)
    
    # Get client's UID and client hello message
    # print('auth_request.state:', auth_request.state.user)
    auth_uid = auth_request.state.user["uid"]
    client_uid = request.client_uid
    if auth_uid != client_uid:
        return JSONResponse(content={"message": "Unauthorized. UID does not match."}, status_code=403)

    # Generate a session ID
    session_id = request.sessionID
    session_keys[client_uid] = {
        'session_id': session_id,
        'session_key': None
    }

    # Handle client hello and respond with server hello
    server_hello_response = {
        'server_hello': 'Hello from CA Server',
    }
    return JSONResponse(content=server_hello_response, status_code=200)

@router.post("/key_exchange")
async def key_exchange():
    try:
        ca_public_key = load_ca_public_key()
        key_exchange_response = {
            'key_exchange': ca_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        }
        return JSONResponse(content=key_exchange_response, status_code=200)
    except FileNotFoundError as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@router.post("/store_session_key")
async def store_session_key(request: EncryptedPayloadRequest):
    try:
        encrypted_payload_base64 = request.data

        # Decode the base64 encoded payload
        encrypted_payload = base64.b64decode(encrypted_payload_base64)
        ca_private_key = load_ca_private_key()
        decrypted_payload = ca_private_key.decrypt(
                encrypted_payload,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=crypto_hash_algo),
                    algorithm=crypto_hash_algo,
                    label=None
                )
            )

        # Convert the decrypted payload from bytes to a string
        decrypted_payload_str = decrypted_payload.decode('utf-8')

        # Parse the JSON string to extract the payload
        payload = json.loads(decrypted_payload_str)
        print(payload)

        session_id = payload.get('session_id')
        session_key = payload.get('session_key')
        client_uid = payload.get('client_uid')
        

        if client_uid not in session_keys:
            return JSONResponse(content={"message": "Session ID not found."}, status_code=400)
            

        # session_keys[session_id]['session_key'] = base64.b64decode(session_key.encode())
        session_keys[client_uid]['session_key'] = session_key
        # print('`session_keys`:', session_keys)
        return JSONResponse(content={"message": "Session key stored successfully."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
