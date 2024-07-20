from fastapi import FastAPI
from middleware.verifyToken import FirebaseAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from middleware.firebase_config import firebaseConfig
from middleware.encryptDecrypt import EncryptMiddleware, DecryptMiddleware
from routes import challenge, handshake
from utils.key import generate_ca_key_pair

firebase_admin.initialize_app(options=firebaseConfig)
from db.db_insert import insert_key_certi

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

generate_ca_key_pair()

routers = [
    handshake.router,
    challenge.router
]


@app.get("/")
async def index():
    return {"message": "CA Server is running."}

for router in routers:
    app.include_router(router)

