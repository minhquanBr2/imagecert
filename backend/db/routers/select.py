from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from schemas.request_schemas import RequestRetrieveImage, RequestRetrievePublicKeyCerti
from db import db_select


router = APIRouter(
    prefix = '/select',
    tags = ['select'],
)


@router.get("/key_certi/{user_uid}")
async def select_key_certi(user_uid: str):
    print(f"Retrieving public key certificate corresponding with user {user_uid}...")
    
    try:
        results = db_select.select_key_certi_from_user_uid(user_uid)
        if results == None:
            return {"message": "No public key certificate found for this user."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/image/original/{image_id}")
async def select_image_original_filename(image_id: int):
    print(f"Retrieving image {image_id}...")
    
    try:
        results = db_select.select_image(image_id, ['originalFilename'])
        if results == None or results == []:
            return {"message": f"Image with ID {image_id} not found."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")