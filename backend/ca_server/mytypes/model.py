from pydantic import BaseModel

class ClientHelloRequest(BaseModel):
    client_hello: str
    client_uid: str
    sessionID: str

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
    session_id: str

class EncryptedPayloadRequest(BaseModel):
    data: str

class PublicKeyRequest(BaseModel):
    user_public_key: str

class CSRRequest(BaseModel):
    csr: str