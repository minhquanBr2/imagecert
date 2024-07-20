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

router = APIRouter(
    prefix = '/zkp',
    tags = ['zkp'],
)

# Store for challenges associated with public keys
challenge_store = {}


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
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
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
    public_key_der = base64.b64decode(user_public_key_pem)
    user_public_key = serialization.load_der_public_key(
        public_key_der,
        backend=default_backend()
    )
    challenge_response = base64.b64decode(data.get("challenge_response"))

    if user_uid not in challenge_store:
        return JSONResponse(content={"message": "Challenge not found for the provided public key."}, status_code=400)
        
        

    challenge = challenge_store.pop(user_uid)  # Get the stored challenge

    
    if challenge_response != challenge:
        return JSONResponse(content={"message": "Verification failed. Challenge response does not match the challenge."}, status_code=400)
    
    
    # CALL REQUEST TO CHECK IF CERTI IS IN DB
    
    # CERTI IS NOT IN DB => SIGN  
    
    ca_private_key = load_ca_private_key()
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"HCMCity"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"HCMUS"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HCMUSMHUD"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"myca.example.com"),
    ])

    not_before = datetime.utcnow()
    not_after = datetime.utcnow() + timedelta(days=365)
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        user_public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        not_before
    ).not_valid_after(
        not_after
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())

    cert_der = cert.public_bytes(serialization.Encoding.DER)
    cert_base64 = base64.b64encode(cert_der).decode('utf-8')
    not_before_timestamp = not_before.isoformat()
    not_after_timestamp = not_after.isoformat()

    # Convert issuer to string
    issuer_string = issuer.rfc4514_string()
    certi_payload = {
        "user_uid": user_uid,
        "issuer_name": issuer_string,
        "not_before": not_before_timestamp,
        "not_after": not_after_timestamp,
        "status": "1",
        "certi_url": cert_base64,
        "public_key": user_public_key_pem
    }

    print('certi_payload', certi_payload)

    db_response = insertKeyCerti(certi_payload)
    print('db_response', db_response)

    return db_response

    # CERTI IS IN DB => VERIFY  
