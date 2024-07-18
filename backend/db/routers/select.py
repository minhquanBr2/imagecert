from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from schemas.request_schemas import RequestRetrievePublicKeyCerti
from db import db_select
import json


router = APIRouter(
    prefix = '/select',
    tags = ['select'],
)


@router.post("/key_certi")
async def select_key_certi(request: RequestRetrievePublicKeyCerti):
    user_uid = request.user_uid
    print(f"Retrieving public key certificate corresponding with user {user_uid}...")
    
    try:
        results = db_select.select_key_certi_from_user_uid(user_uid)
        if results == None:
            return {"message": "No public key certificate found for this user."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")