from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
import os
import base64
from utils.key import generate_ca_key_pair, load_ca_private_key, load_ca_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from middleware.verifyToken import FirebaseAuthMiddleware
from middleware.encryptDecrypt import session_keys
from fastapi.middleware.cors import CORSMiddleware
from db.db_insert import insert_key_certi

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(FirebaseAuthMiddleware)



class PublicKeyRequest(BaseModel):
    user_public_key: str

class VerifyRequest(BaseModel):
    user_public_key: str
    challenge_response: str

class CSRRequest(BaseModel):
    csr: str

generate_ca_key_pair()
# Store for challenges associated with public keys
challenge_store = {}

@app.get("/")
async def index():
    return {"message": "CA Server is running."}

@app.post("/challenge")
async def challenge_endpoint(request: PublicKeyRequest):
    user_public_key_pem = request.user_public_key
    user_public_key = serialization.load_pem_public_key(
        user_public_key_pem.encode(),
        backend=serialization.DefaultBackend()
    )

    challenge = os.urandom(32)  # Generate a random challenge
    challenge_store[user_public_key_pem] = challenge  # Store the challenge for later verification

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

@app.post("/verify")
async def verify_endpoint(request: VerifyRequest):
    user_public_key_pem = request.user_public_key
    challenge_response = base64.b64decode(request.challenge_response)

    if user_public_key_pem not in challenge_store:
        raise HTTPException(status_code=400, detail="Challenge not found for the provided public key.")

    challenge = challenge_store.pop(user_public_key_pem)  # Get the stored challenge

    user_public_key = serialization.load_pem_public_key(
        user_public_key_pem.encode(),
        backend=serialization.DefaultBackend()
    )

    try:
        # Verify the response is the decrypted challenge
        user_public_key.verify(
            challenge_response,
            challenge,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Verification failed: " + str(e))

    # Proceed to sign the certificate
    ca_private_key = load_ca_private_key()
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"HCMCity"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"HCMUS"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HCMUSMHUD"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"myca.example.com"),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        user_public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())

    # TODO: SAVE CERTI TO CERTI DB
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    insert_key_certi(
        userUID = request.state.user, 
        certiURL = cert_pem, 
        issuerName = "", 
        notBefore = "", 
        notAfter = "", 
        status = "", 
        publicKey = user_public_key_pem)

    return {"certificate": cert_pem}


class ClientHelloRequest(BaseModel):
    client_hello: str
    client_uid: str

class ServerHelloResponse(BaseModel):
    server_hello: str
    server_public_key: str

class KeyExchangeResponse(BaseModel):
    key_exchange: str

class VerifyRequest(BaseModel):
    session_id: str
    encrypted_message: str

class SessionInfo(BaseModel):
    client_uid: str
    session_key: str

@app.post("/client_hello")
async def client_hello(request: ClientHelloRequest):
    if request.client_hello != 'Hello from Client':
        raise HTTPException(status_code=400, detail="Invalid client hello message.")

    if not request.state.user:
        raise HTTPException(status_code=403, detail="Unauthorized. User not authenticated.")
    
    # Get client's UID and client hello message
    auth_uid = request.state.user.uid
    client_uid = request.client_uid
    if auth_uid != client_uid:
        raise HTTPException(status_code=403, detail="Unauthorized. UID does not match.")

    # Get sessionn ID
    session_id = request.session_id
    session_keys[session_id] = {
        'client_uid': client_uid,
        'session_key': None
    }
    # Handle client hello and respond with server hello
    server_hello_response = {
        'server_hello': 'Hello from CA Server',
    }
    return server_hello_response

@app.post("/key_exchange")
async def key_exchange():
    # Respond with CA server's public key
    try:
        ca_public_key = load_ca_public_key()
        key_exchange_response = {
            'key_exchange': ca_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        }
        return key_exchange_response
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store_session_key")
async def store_session_key(request: SessionInfo):
    session_id = request.session_id
    client_uid = request.client_uid
    session_key = request.session_key

    if session_id not in session_keys:
        raise HTTPException(status_code=400, detail="Session ID not found.")
    
    # decrypt the session key using ca private key
    ca_private_key = load_ca_private_key()
    session_key = ca_private_key.decrypt(
        base64.b64decode(session_key.encode()),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    session_keys[session_id]['session_key'] = base64.b64decode(session_key.encode())
    print('`session_keys`:', session_keys)
    return {"message": "Session key stored successfully."}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
