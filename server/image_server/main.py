from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, admin_verify
from middlewares.firebase.firebase_middleware import FirebaseAuthMiddleware
from firebase_admin import credentials, get_app
from config import FIREBASE_ADMIN_SDK, PERM_IMAGE_DIR, TLS_CERT, TLS_KEY
import firebase_admin
import ssl


# Initialize Firebase Admin SDK
try:
    appAdminSDK = get_app("appAdminSDK")
    print("Firebase Admin SDK already initialized.")
except ValueError:
    print("Initializing Firebase Admin SDK...")
    cred = credentials.Certificate(FIREBASE_ADMIN_SDK)
    firebase_admin.initialize_app(credential=cred, name="appAdminSDK")
    print("Firebase Admin SDK initialized.")


# Initialize FastAPI app and mount the images directory
app = FastAPI()
app.mount("/image", StaticFiles(directory=PERM_IMAGE_DIR), name="images")            # Mount the images directory to serve static files


# # Initialize SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(TLS_CERT, keyfile=TLS_KEY)


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
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, ssl_keyfile=TLS_KEY, ssl_certfile=TLS_CERT)
