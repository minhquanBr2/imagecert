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
import json


# Load environment variables
CRED_USER_PATH = os.getenv('CRED_USER_PATH')
CRED_ADMIN_PATH = os.getenv('CRED_ADMIN_PATH')

# appUserSDK
try:
    credUser = credentials.Certificate(CRED_USER_PATH)
    firebase_admin.initialize_app(credUser, name="appUserSDK")
    appUserSDK = get_app("appUserSDK")
    print("appUserSDK initialized successfully.")
except ValueError as e:
    appUserSDK = get_app("appUserSDK")  # App is already initialized
    print("appUserSDK is already initialized.")
except Exception as e:
    print(f"Error initializing appUserSDK: {e}")

# appAdminSDK
try:
    credAdmin = credentials.Certificate(CRED_ADMIN_PATH)
    firebase_admin.initialize_app(credAdmin, name="appAdminSDK")
    appAdminSDK = get_app("appAdminSDK")
    print("appAdminSDK initialized successfully.")
except ValueError as e:
    try:
        appAdminSDK = get_app("appAdminSDK")  
        print("appAdminSDK is already initialized.")
    except Exception as e:
        print(f"Error initializing appAdminSDK: {e}")


# Initialize FastAPI app
app = FastAPI()
 
 
# Mount the images directory
if not os.path.exists(PERM_IMAGE_DIR):
    os.makedirs(PERM_IMAGE_DIR)
    print(f"Directory {PERM_IMAGE_DIR} created.")    
app.mount("/image", StaticFiles(directory=PERM_IMAGE_DIR), name="images")            # Mount the images directory to serve static files


# # Initialize SSL context
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(TLS_CERT_PATH, keyfile=TLS_KEY_PATH)


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
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
