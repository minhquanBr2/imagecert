from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import firebase_admin
from firebase_admin import auth, credentials
import jwt
from firebase_config import firebaseConfig

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("./imageca-6c45f-firebase-adminsdk-c5nuc-c8a9b39828.json")
firebase_admin.initialize_app(cred, firebaseConfig)

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")

        if authorization:
            token = authorization.split(" ")[1]
            try:
                decoded_token = auth.verify_id_token(token)
                request.state.user = decoded_token
            except (auth.InvalidIdTokenError, auth.ExpiredIdTokenError, jwt.PyJWTError):
                raise HTTPException(status_code=401, detail="Invalid token")

        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        response = await call_next(request)
        return response
