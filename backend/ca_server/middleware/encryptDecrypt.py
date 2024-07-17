from fastapi import FastAPI, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from shared import session_keys


# Middleware to decrypt incoming requests using session key
async def decrypt_request(request: Request, response: Response):
    session_id = request.headers.get('X-Session-ID')
    if session_id and session_id in session_keys:
        session_key = session_keys[session_id]
        encrypted_body = await request.body()
        if encrypted_body:
            cipher = Cipher(algorithms.AES(session_key), modes.CBC(IV=b'0123456789abcdef'), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_body = decryptor.update(encrypted_body) + decryptor.finalize()
            request._body = decrypted_body
    else:
        raise HTTPException(status_code=400, detail="Invalid or missing session ID")

# Middleware to encrypt outgoing responses using session key
async def encrypt_response(request: Request, call_next):
    response = await call_next(request)

    session_id = request.headers.get('X-Session-ID')
    if session_id and session_id in session_keys:
        session_key = session_keys[session_id]
        if response.body:
            cipher = Cipher(algorithms.AES(session_key), modes.CBC(IV=b'0123456789abcdef'), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_body = encryptor.update(response.body) + encryptor.finalize()
            response.body = encrypted_body

    return response

import os
import json
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from shared import session_keys

# Middleware to decrypt request
class DecryptMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                data = json.loads(body)
                session_key = request.headers.get("X-Session-Key")
                if session_key and "iv" in data and "payload" in data and "tag" in data:
                    iv = b64decode(data["iv"])
                    encrypted_payload = b64decode(data["payload"])
                    tag = b64decode(data["tag"])
                    
                    cipher = AES.new(b64decode(session_key), AES.MODE_GCM, iv)
                    decrypted_payload = cipher.decrypt_and_verify(encrypted_payload, tag)
                    
                    request._body = decrypted_payload
                    request.headers["content-length"] = str(len(decrypted_payload))

        response = await call_next(request)
        return response

# Middleware to encrypt response
class EncryptMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 200 and response.headers.get("content-type") == "application/json":
            session_key = request.headers.get("X-Session-Key")
            if session_key:
                data = await response.body()
                if data:
                    iv = get_random_bytes(12)
                    cipher = AES.new(b64decode(session_key), AES.MODE_GCM, iv)
                    encrypted_payload, tag = cipher.encrypt_and_digest(data)
                    
                    encrypted_response = {
                        "iv": b64encode(iv).decode(),
                        "payload": b64encode(encrypted_payload).decode(),
                        "tag": b64encode(tag).decode()
                    }
                    
                    return Response(
                        content=json.dumps(encrypted_response),
                        media_type="application/json",
                        status_code=response.status_code
                    )
        return response

