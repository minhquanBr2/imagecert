from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.firebase_auth import FirebaseAuthMiddleware
from middlewares.firebase_init import initialize_firebase
from routers import insert, select


app = FastAPI()


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# # Set up Firebase Auth middleware
# initialize_firebase()
# app.add_middleware(FirebaseAuthMiddleware)


# Add routers
routers = [
    insert.router,
    select.router
]
for router in routers:
    app.include_router(router)