from fastapi import FastAPI
from middleware.verifyToken import FirebaseAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from middleware.firebaseConfig import firebaseConfig
from middleware.encryptDecrypt import EncryptMiddleware, DecryptMiddleware
from routes import challenge, handshake
from utils.key import generate_ca_key_pair
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('../cert.pem', keyfile='../key.pem')

generate_ca_key_pair()

firebase_admin.initialize_app(options=firebaseConfig)

app = FastAPI()

# Add CORS middleware
app.add_middleware(FirebaseAuthMiddleware)
app.add_middleware(EncryptMiddleware)
app.add_middleware(DecryptMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)



routers = [
    handshake.router,
    challenge.router
]


@app.get("/")
async def index():
    return {"message": "CA Server is running."}

for router in routers:
    app.include_router(router)

