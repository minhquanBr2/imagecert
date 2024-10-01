from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import auth
from fastapi.responses import JSONResponse
from firebase_admin import get_app

exclude_paths = [
    "/docs",
    "/redoc",
    "/openapi.json",
]



class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Allow OPTIONS requests to pass through
        if request.method == "OPTIONS":
            return await call_next(request)

        # Exclude SwaggerUI and Redoc paths
        for exclude_path in exclude_paths:
            if request.url.path.startswith(exclude_path):
                return await call_next(request)
        
        token = request.headers.get("Authorization")

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )
        
        token = token.split("Bearer ")[-1]
        try:
            decoded_token = auth.verify_id_token(token, app=get_app("appUser"))
            request.state.user = decoded_token
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Invalid or expired token: {str(e)}"}
            )

        response = await call_next(request)
        return response
