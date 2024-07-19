from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from schemas.request_schemas import RequestUploadPublicKeyCerti
from db import db_insert


router = APIRouter(
    prefix = '/insert',
    tags = ['insert'],
)


@router.post("/key_certi")
async def insert_key_certi(request: RequestUploadPublicKeyCerti):
    user_uid = request.user_uid
    certi = request.certi
    issuer_name = request.issuer_name
    not_before = request.not_before
    not_after = request.not_after
    status = request.status
    public_key = request.public_key
    print(f"Public key {public_key[:10]}...{public_key[-10:]} received from user {user_uid}.")
    
    try:
        db_insert.insert_key_certi(user_uid, certi, issuer_name, not_before, not_after, status, public_key)
        return {"message": "Public key registered successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")