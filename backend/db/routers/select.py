from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from schemas.request_schemas import RequestRetrieveImage, RequestRetrievePublicKeyCerti
from db import db_select


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


@router.post("/image")
async def select_image(request: RequestRetrieveImage):
    image_id = request.image_id
    attributes = request.attributes
    print(f"Retrieving image {image_id}...")
    
    try:
        results = db_select.select_image(image_id, attributes)
        if results == None:
            return {"message": f"Image {image_id} not found."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")