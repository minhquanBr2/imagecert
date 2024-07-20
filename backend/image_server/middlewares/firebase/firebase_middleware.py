from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from middlewares.firebase.firebase_init import appUser, appAdmin
from firebase_admin import auth


exclude_paths = [
    "/docs",
    "/redoc",
    "/openapi.json",
    "/image"
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
        
        try:
            token = request.headers.get("authorization").split("Bearer ")[-1]
            print(f"Token: {token[:10]}...{token[-10:]}")
        except:
            raise HTTPException(status_code=401, detail="Authorization token missing")            
        
        try:
            if request.url.path.startswith("/upload"):
                decoded_token = auth.verify_id_token(token, appUser)
            else:
                decoded_token = auth.verify_id_token(token, appAdmin)
            request.state.user = decoded_token
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

        response = await call_next(request)
        return response


# async def firebase_auth_user_middleware(request: Request, call_next):
#     print(f"Request headers: {request.headers}")
#     # Allow OPTIONS requests to pass through
#     if request.method == "OPTIONS":
#         return await call_next(request)

#     # Exclude SwaggerUI and Redoc paths
#     for exclude_path in exclude_paths:
#         if request.url.path.startswith(exclude_path):
#             return await call_next(request)
    
#     print(f"Request headers: {request.headers}")
#     token = request.headers.get("authorization").split("Bearer ")[-1]
#     print(f"Token: {token[:10]}...{token[-10:]}")

#     if not token:
#         raise HTTPException(status_code=401, detail="Authorization token missing")
    
#     try:
#         decoded_token = auth.verify_id_token(token, app=appUser)
#         request.state.user = decoded_token
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

#     response = await call_next(request)
#     return response


# async def firebase_auth_admin_middleware(request: Request, call_next):
#     # Allow OPTIONS requests to pass through
#     if request.method == "OPTIONS":
#         return await call_next(request)

#     # Exclude SwaggerUI and Redoc paths
#     for exclude_path in exclude_paths:
#         if request.url.path.startswith(exclude_path):
#             return await call_next(request)
    
#     token = request.headers.get("authorization").split("Bearer ")[-1]
#     print(f"Token: {token[:10]}...{token[-10:]}")

#     if not token:
#         raise HTTPException(status_code=401, detail="Authorization token missing")
    
#     try:
#         decoded_token = auth.verify_id_token(token, app=appAdmin)
#         request.state.user = decoded_token
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

#     response = await call_next(request)
#     return response


# class FirebaseAuthAdminMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):

#         # Allow OPTIONS requests to pass through
#         if request.method == "OPTIONS":
#             return await call_next(request)

#         # Exclude SwaggerUI and Redoc paths
#         for exclude_path in ['docs', 'redoc', 'openapi.json', 'upload']:
#             if request.url.path.startswith(exclude_path):
#                 return await call_next(request)
        
#         token = request.headers.get("authorization").split("Bearer ")[-1]
#         print(f"Admin token: {token[:10]}...{token[-10:]}")

#         if not token:
#             raise HTTPException(status_code=401, detail="Authorization token missing")
        
#         try:
#             decoded_token = auth.verify_id_token(token, app=appAdmin)
#             request.state.user = decoded_token
#         except Exception as e:
#             raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

#         response = await call_next(request)
#         return response
