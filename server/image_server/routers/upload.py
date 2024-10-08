from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import sys 
sys.path.append('..')
from internal.upload.save import save_uploaded_data_to_db, save_webp_image, save_temp_image
from internal.upload.self_verify import self_verify_image
import config
import requests


router = APIRouter(
    prefix = '/upload',
    tags = ['upload']
)


@router.post("/image")
async def upload_image(request: Request, signature: str = Form(...), file: UploadFile = File(...)):
    user_uid = request.state.user['uid']                                    # Access the user UID from Firebase token
    print(f"File {file.filename} received from user {user_uid}.")
    
    try:         
        original_filename, filename, temp_filepath = save_temp_image(file)
        verification_status, hash_object, ref_image_ids = await self_verify_image(temp_filepath)
        print(f"Verification status: {verification_status}.")

        if verification_status == config.VERIFICATION_STATUS["ACCEPTED"]:
            perm_filepath = save_webp_image(temp_filepath)
            await save_uploaded_data_to_db(user_uid, original_filename, filename, temp_filepath, signature, verification_status, hash_object, ref_image_ids)
            return {"message": f"Image {original_filename} registered successfully."}
        elif verification_status == config.VERIFICATION_STATUS["PENDING"]:
            perm_filepath = save_webp_image(temp_filepath)
            await save_uploaded_data_to_db(user_uid, original_filename, filename, perm_filepath, signature, verification_status, hash_object, ref_image_ids)
            return {"message": f"Image {original_filename} is under consideration."}
        else:
            return JSONResponse(status_code=409, content={"message": f"Image {original_filename} is rejected."})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/get_all")
async def get_all_images():
    url = f"{config.DB_ENDPOINT_URL}/select/all_images"
    response = requests.get(url)
    if response.status_code != 200:
        return {"message": f"Internal server error with status code {response.status_code}."}

    results = response.json()["message"]
    if len(results) == 0:
        return {"message": "No images found."}

    return results
