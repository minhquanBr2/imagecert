from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import auth


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
        
        print("middleware request headers: ", request.headers)
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=401, detail="Authorization token missing")
        
        token = token.split("Bearer ")[-1]
        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

        response = await call_next(request)
        return response
