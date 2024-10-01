from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from shared import session_keys

# Generate and store CA's key pair if not already present
def generate_ca_key_pair():
    if not os.path.exists('ca_private_key.pem') or not os.path.exists('ca_public_key.pem'):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        with open('ca_private_key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open('ca_public_key.pem', 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))


# Load CA's private key
def load_ca_private_key():
    if os.path.exists('ca_private_key.pem'):
        with open('ca_private_key.pem', 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        return private_key
    else:
        generate_ca_key_pair()
        load_ca_private_key()

def load_ca_public_key():
    if os.path.exists('ca_public_key.pem'):
        with open('ca_public_key.pem', 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        return public_key
    else:
        generate_ca_key_pair()
        raise FileNotFoundError("CA public key file not found.")

def store_session_key(session_id: str, encrypted_session_key: str):
    # Store encrypted session key with session ID
    session_keys[session_id] = base64.b64decode(encrypted_session_key.encode())


if __name__ == "__main__":
    generate_ca_key_pair()
