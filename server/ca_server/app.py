from fastapi import FastAPI
from middleware.verifyToken import FirebaseAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from middleware.firebaseConfig import firebaseConfig
from middleware.encryptDecrypt import EncryptMiddleware, DecryptMiddleware
from routes import challenge, handshake
from utils.key import generate_ca_key_pair
import ssl
from firebase_admin import get_app

TLS_KEY = '/home/khang/imagecert/server/key.pem'
TLS_CERT = '/home/khang/imagecert/server/cert.pem'

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(TLS_CERT, keyfile=TLS_KEY)

generate_ca_key_pair()



try:
    appAdminSDK = get_app("appUserSDK")
    print("Firebase Admin SDK already initialized.")
except ValueError:
    print("Initializing Firebase Admin SDK...")
    firebase_admin.initialize_app(options=firebaseConfig, name="appUserSDK")
    print("Firebase Admin SDK initialized.")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True, ssl_keyfile=TLS_KEY, ssl_certfile=TLS_CERT)