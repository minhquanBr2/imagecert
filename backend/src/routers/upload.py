from fastapi import APIRouter, status, HTTPException, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import sys 
sys.path.append('..')
from internal.upload.save import save_uploaded_data_to_db
from internal.upload.self_verify import self_verify_image
import os
import config


router = APIRouter(
    prefix = '/upload',
    tags = ['upload'],
)


@router.post("/image")
async def upload_image(userUID: int = Form(...), file: UploadFile = File(...)):
    userUID = 2
    print(f"File {file.filename} received from user {userUID}.")
    try: 
        filepath = os.path.join(config.IMAGE_DIR, file.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())
        file.file.close()
        verification_status, hash_object, ref_filepath = self_verify_image(filepath)
        print(f"Verification status: {verification_status}.")

        if verification_status == config.VERIFICATION_STATUS["ACCEPT"]:
            save_uploaded_data_to_db(userUID, filepath, verification_status, hash_object)
            # TODO: prompt user to select private key file, next request only need to send the signature
            return {"message": "Image registered successfully. Please sign the image."}
        elif verification_status == config.VERIFICATION_STATUS["CONSIDER"]:
            save_uploaded_data_to_db(userUID, filepath, verification_status, hash_object)
            return {"message": "Image is under consideration."}
        else:
            return {"message": f"Image is rejected. A reference image can be found at {ref_filepath}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")