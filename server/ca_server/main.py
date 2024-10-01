from fastapi import FastAPI
from middleware.verifyToken import FirebaseAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from middleware.encryptDecrypt import EncryptMiddleware, DecryptMiddleware
from routes import challenge, handshake
from utils.key import generate_ca_key_pair
import ssl
import os
import json
from firebase_admin import credentials, get_app


# TLS_KEY_PATH = os.getenv('TLS_KEY_PATH')
# TLS_CERT_PATH = os.getenv('TLS_CERT_PATH')
# FIREBASE_ADMIN_SDK_PATH = os.getenv('FIREBASE_ADMIN_SDK_PATH')
FIREBASE_CONFIGS_PATH = os.getenv('FIREBASE_CONFIGS_PATH')
CRED_USER_PATH = os.getenv('CRED_USER_PATH')
with open(FIREBASE_CONFIGS_PATH, 'r') as f:
    config_data = json.load(f)
firebaseConfigAdmin = config_data["firebaseConfigAdmin"]
firebaseConfigUser = config_data["firebaseConfigUser"]


# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(TLS_CERT_PATH, keyfile=TLS_KEY_PATH)

generate_ca_key_pair()


# # AdminSDK
# print("Initializing Firebase Admin SDK...")
# try:
#     app = get_app("AdminSDK")
#     print("Firebase Admin SDK is already initialized.")
# except ValueError:
#     cred = credentials.Certificate(FIREBASE_ADMIN_SDK_PATH)
#     firebase_admin.initialize_app(cred, name="AdminSDK")
#     print("Firebase Admin SDK initialized successfully.")

# # appAdmin
# try:
#     print(f"firebaseConfigAdmin: {firebaseConfigAdmin}")
#     appAdmin = get_app("appAdmin")
#     print("App Admin is already initialized.")
# except ValueError:
#     try:
#         firebase_admin.initialize_app(options=firebaseConfigAdmin, name="appAdmin")
#         appAdmin = get_app("appAdmin")
#         print("App Admin initialized successfully.")
#     except Exception as e:
#         print(f"Error initializing App Admin: {e}")

# UserSDK



# appUser
try:
    credUser = credentials.Certificate(CRED_USER_PATH)
    firebase_admin.initialize_app(credUser, name="appUser")
    appUser = get_app("appUser")
    print("App User initialized successfully.")
except ValueError as e:
    appUser = get_app("appUser")  # App is already initialized
    print("App User is already initialized.")
except Exception as e:
    print(f"Error initializing App User: {e}")
# try:
#     print(f"firebaseConfigUser: {firebaseConfigUser}")
#     appUser = get_app("appUser")
#     print("App User is already initialized.")
# except ValueError:
#     try:
#         firebase_admin.initialize_app(options=firebaseConfigUser, name="appUser")
#         appUser = get_app("appUser")
#         print("App User initialized successfully.")
#     except Exception as e:
#         print(f"Error initializing App User: {e}")
    
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.add_middleware(FirebaseAuthMiddleware)
app.add_middleware(EncryptMiddleware)
app.add_middleware(DecryptMiddleware)



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
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
