from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
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


@router.get("/verification_history/{admin_uid}")
async def select_verification_history(admin_uid: str):
    print(f"Retrieving verification history for admin {admin_uid}...")
    
    try:
        results = db_select.select_verification_history(admin_uid)
        if results == None or results == []:
            return {"message": "No verification history found for this admin."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/pending_images")
async def select_pending_images():
    print("Retrieving pending images...")
    
    try:
        results = db_select.select_pending_images()
        if results == None or results == []:
            return {"message": "No pending images found."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/all_images")
async def select_all_images():
    print("Retrieving all images...")
    
    try:
        results = db_select.select_all_images()
        if results == None or results == []:
            return {"message": "No images found."}
        return {"message": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/image/{image_id}/user_uid")
async def select_image_user_uid(image_id: int):
    print(f"Retrieving user UID for image {image_id}...")
    
    try:
        results = db_select.select_user_uid_from_image_id(image_id)
        if results == None:
            return {"message": f"Image with ID {image_id} not found."}
        return {"message": results}

    except Exception as e:
        raise JSONResponse(status_code=500, content=f"Internal server error: {str(e)}")


@router.get("/all_hashes")
async def select_all_hashes():
    print("Retrieving all hashes...")
    
    try:
        results = db_select.select_all_hashes()
        if results == None or results == []:
            return {"message": "No hashes found."}
        return {"message": results}

    except Exception as e:
        raise JSONResponse(status_code=500, content=f"Internal server error: {str(e)}")

    