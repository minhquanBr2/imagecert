from fastapi import FastAPI
from routers import upload


app = FastAPI()


# Add routers
routers = [
    upload.router,
]
for router in routers:
    app.include_router(router)
