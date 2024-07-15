from fastapi import FastAPI
from routers import upload
from middlewares.firebase_auth import FirebaseAuthMiddleware
from internal.firebase_config import initialize_firebase


app = FastAPI()


initialize_firebase()
app.add_middleware(FirebaseAuthMiddleware)


# Add routers
routers = [
    upload.router,
]
for router in routers:
    app.include_router(router)
