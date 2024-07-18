import os
import json
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from firebase_admin import auth
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from shared import session_keys
from typing import Callable

def get_uid_from_authorization_header(authorization: str):
    if authorization:
        token = authorization.split(" ")[1]
        token = token.split("Bearer ")[-1]
        decoded_token = auth.verify_id_token(token)
        print('get_uid_from_authorization_header', decoded_token)
        return decoded_token.get("uid")
    return None

# Middleware to decrypt request
class DecryptMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                data = json.loads(body)
                uid = get_uid_from_authorization_header(request.headers.get("Authorization"))
                session_key = None
                if session_keys and session_keys[uid]:
                    session_key = session_keys[uid]["session_key"]
                if session_key and "iv" in data and "payload" in data and "tag" in data:
                    print('DecryptMiddleware', uid, session_key, session_keys)  
                    iv = b64decode(data["iv"])
                    encrypted_payload = b64decode(data["payload"])
                    tag = b64decode(data["tag"])
                    
                    cipher = AES.new(b64decode(session_key), AES.MODE_GCM, iv)
                    decrypted_payload = cipher.decrypt_and_verify(encrypted_payload, tag)
                    
                    request.state.decrypted_payload = decrypted_payload

        response = await call_next(request)
        return response

# Middleware to encrypt response
class EncryptMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)

        if response.status_code == 200 and response.headers.get("content-type") == "application/json":
            uid = get_uid_from_authorization_header(request.headers.get("Authorization"))
            session_key = None
            if session_keys and uid in session_keys:
                session_key = session_keys[uid]["session_key"]

            if session_key:
                print('EncryptMiddleware', uid, session_key, session_keys)
                
                # Read response content
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk

                if body:
                    iv = get_random_bytes(12)
                    cipher = Cipher(algorithms.AES(b64decode(session_key)), modes.GCM(iv))
                    encryptor = cipher.encryptor()
                    encrypted_payload = encryptor.update(body) + encryptor.finalize()

                    encrypted_response = {
                        "iv": b64encode(iv).decode(),
                        "payload": b64encode(encrypted_payload).decode(),
                        "tag": b64encode(encryptor.tag).decode()
                    }

                    print("Encrypted Response:", encrypted_response)

                    # Create the new response
                    m_response = Response(
                        content=json.dumps(encrypted_response),
                        media_type="application/json",
                        status_code=response.status_code
                    )

                    # Copy CORS headers from the original response
                    for key, value in response.headers.items():
                        if key.lower().startswith("access-control-"):
                            m_response.headers[key] = value

                    return m_response

        return response