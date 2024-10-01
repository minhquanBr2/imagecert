from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.request_schemas import RequestUploadImage, RequestUploadHash, RequestUploadVerificationStatus, RequestUploadPublicKeyCerti, RequestUploadRef
import db_insert, db_select, db_update


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
        image_id = await db_insert.insert_image(user_uid, original_filename, filename, timestamp, caption, location, device_name, signature, ref_filepath)
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
        await db_insert.insert_hash(image_id, hash_type, value)
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
        await db_insert.insert_verification_status(image_id, admin_uid, result, verification_timestamp)
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
    
    try:
        print(f"user_uid: {user_uid}")
        all_key_certis = await db_select.select_all_key_certis_from_user_uid(user_uid)
        curr_key_certi = {}
        # check if the new certi existed:
        if all_key_certis:
            for key_certi in all_key_certis:
                if key_certi["status"] == 1:
                    curr_key_certi = key_certi
                if key_certi["public_key"] == public_key and key_certi["status"] == 1:
                    return JSONResponse(status_code=200, content="Public key already exists and is active.")
                elif key_certi["public_key"] == public_key and key_certi["status"] == 0:
                    return JSONResponse(status_code=401, content="Public key already exists but is inactive.")          
            # key does not exist, set the status of the current key from 1 to 0, and insert new key
            if curr_key_certi:
                await db_update.update_key_certi(curr_key_certi["certi_id"], ["status"], [0])
                print('user_uid: ', user_uid)
                print('certi: ', certi[0:20] + '...' + certi[-20:])
                print('issuer_name: ', issuer_name)
                print('not_before: ', not_before)
                print('not_after: ', not_after)
                print('status: ', status)
                print('public_key: ', public_key[0:20] + '...' + public_key[-20:])
                await db_insert.insert_key_certi(user_uid, certi, issuer_name, not_before, not_after, status, public_key)
                print("Public key registered successfully.")
                return JSONResponse(status_code=200, content="Public key registered successfully.")
            else:
                print("An error occured when storing key certificate into DB.")
                return JSONResponse(status_code=500, content="An error occured when storing key certificate into DB.")
        else:
            await db_insert.insert_key_certi(user_uid, certi, issuer_name, not_before, not_after, status, public_key)
            print("Public key registered successfully.")
            return JSONResponse(status_code=200, content="Public key registered successfully.")

    except Exception as e:
        return JSONResponse(status_code=500, content=f"Internal server error: {str(e)}")


@router.post("/ref")
async def insert_ref(request: RequestUploadRef):
    image_id = request.image_id
    ref_image_id = request.ref_image_id
    print(f"Reference image {ref_image_id} received for image with id {image_id}.")
    
    try:
        await db_insert.insert_ref(image_id, ref_image_id)
        return {"message": "Added new reference."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")