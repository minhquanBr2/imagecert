from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, admin_verify
from middlewares.firebase.firebase_middleware import FirebaseAuthMiddleware
import firebase_admin
from internal.firebase.config import firebaseConfig

firebase_admin.initialize_app(options=firebaseConfig)

app = FastAPI()
app.mount("/image", StaticFiles(directory="../data/images/perm"), name="images")            # Mount the images directory to serve static files


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
