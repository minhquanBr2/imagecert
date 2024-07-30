from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, admin_verify
from middlewares.firebase.firebase_middleware import FirebaseAuthMiddleware
from firebase_admin import credentials, auth
from config import FIREBASE_ADMIN_SDK, PERM_IMAGE_DIR
import firebase_admin


# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_ADMIN_SDK)
firebase_admin.initialize_app(credential=cred)


# Initialize FastAPI app
app = FastAPI()
app.mount("/image", StaticFiles(directory=PERM_IMAGE_DIR), name="images")            # Mount the images directory to serve static files


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
