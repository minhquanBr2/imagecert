from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import sys 
sys.path.append('..')
from mytypes.model import VerifyRequest, PublicKeyRequest
import os
from middleware.encryptDecrypt import session_keys
from cryptography.hazmat.primitives import serialization, hashes
from utils.key import load_ca_private_key, load_ca_public_key
from cryptography.hazmat.primitives.asymmetric import padding
import base64

router = APIRouter(
    prefix = '/zkp',
    tags = ['zkp'],
)

# Store for challenges associated with public keys
challenge_store = {}


@router.post("/challenge")
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

@router.post("/verify")
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

    return {"certificate": cert_pem}
