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