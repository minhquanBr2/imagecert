from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, admin_verify
from middlewares.firebase_auth import FirebaseAuthMiddleware
from internal.firebase_init import initialize_firebase


app = FastAPI()
app.mount("/image", StaticFiles(directory="../data/images/perm"), name="images")            # Mount the images directory to serve static files


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Set up Firebase Auth middleware
initialize_firebase()
app.add_middleware(FirebaseAuthMiddleware)


# Add routers
routers = [
    upload.router,
    admin_verify.router
]
for router in routers:
    app.include_router(router)
