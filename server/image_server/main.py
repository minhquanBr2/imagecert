from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, admin_verify
from middlewares.firebase.firebase_middleware import FirebaseAuthMiddleware
from firebase_admin import credentials, get_app
from config import PERM_IMAGE_DIR
import firebase_admin
import ssl
import os


# Load environment variables
FIREBASE_ADMIN_SDK_PATH = os.getenv('FIREBASE_ADMIN_SDK_PATH')
TLS_KEY_PATH = os.getenv('TLS_KEY_PATH')
TLS_CERT_PATH = os.getenv('TLS_CERT_PATH')


# Initialize Firebase Admin SDK
try:
    appAdminSDK = get_app("appAdminSDK")
    print("Firebase Admin SDK already initialized.")
except ValueError:
    print("Initializing Firebase Admin SDK...")
    cred = credentials.Certificate(FIREBASE_ADMIN_SDK_PATH)
    firebase_admin.initialize_app(credential=cred, name="appAdminSDK")
    print("Firebase Admin SDK initialized.")


# Initialize FastAPI app
app = FastAPI()
 
 
# Mount the images directory
if not os.path.exists(PERM_IMAGE_DIR):
    os.makedirs(PERM_IMAGE_DIR)
    print(f"Directory {PERM_IMAGE_DIR} created.")    
app.mount("/image", StaticFiles(directory=PERM_IMAGE_DIR), name="images")            # Mount the images directory to serve static files


# Initialize SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(TLS_CERT_PATH, keyfile=TLS_KEY_PATH)


# Add middlewares
app.add_middleware(FirebaseAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Add routers
routers = [
    upload.router,
    admin_verify.router
]
for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, ssl_keyfile=TLS_KEY_PATH, ssl_certfile=TLS_CERT_PATH)
