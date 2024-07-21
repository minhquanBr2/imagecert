from fastapi import APIRouter, HTTPException
from schemas.request_schemas import RequestUploadImage, RequestUploadHash, RequestUploadVerificationStatus, RequestUploadPublicKeyCerti, RequestUploadRef
import db_insert


router = APIRouter(
    prefix = '/insert',
    tags = ['insert'],
)


@router.post("/image")
async def insert_image(request: RequestUploadImage):
    user_uid = request.user_uid
    original_filename = request.original_filename
    filename = request.filename
    timestamp = request.timestamp
    caption = request.caption
    location = request.location
    device_name = request.device_name
    signature = request.signature
    ref_filepath = request.ref_filepath
    print(f"File {original_filename} received from user {user_uid}.")
    
    try:
        image_id = db_insert.insert_image(user_uid, original_filename, filename, timestamp, caption, location, device_name, signature, ref_filepath)
        print("image id: ", image_id)
        return {"message": {
            "image_id": image_id
        }}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/hash")
async def insert_hash(request: RequestUploadHash):
    image_id = request.image_id
    hash_type = request.hash_type
    value = request.value
    print(f"Hash {value} received for image with id {image_id}.")
    
    try:
        db_insert.insert_hash(image_id, hash_type, value)
        return {"message": "Hash registered successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/verification_status")
async def insert_verification_status(request: RequestUploadVerificationStatus):
    image_id = request.image_id
    admin_uid = request.admin_uid
    result = request.result
    verification_timestamp = request.verification_timestamp
    print(f"Verification status {result} received for image with id {image_id}.")
    
    try:
        db_insert.insert_verification_status(image_id, admin_uid, result, verification_timestamp)
        return {"message": "Verification status registered successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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


@router.post("/ref")
async def insert_ref(request: RequestUploadRef):
    image_id = request.image_id
    ref_image_id = request.ref_image_id
    print(f"Reference image {ref_image_id} received for image with id {image_id}.")
    
    try:
        db_insert.insert_ref(image_id, ref_image_id)
        return {"message": "Added new reference."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")