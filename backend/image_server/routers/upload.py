from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
import sys 
sys.path.append('..')
from internal.upload.save import save_uploaded_data_to_db, save_webp_image, save_temp_image
from internal.upload.self_verify import self_verify_image
import config


router = APIRouter(
    prefix = '/upload',
    tags = ['upload'],
)


@router.post("/image")
async def upload_image(request: Request, signature: str = Form(...), file: UploadFile = File(...)):
    user_uid = request.state.user['uid']                                    # Access the user UID from Firebase token
    print(f"File {file.filename} received from user {user_uid}.")
    
    try:         
        original_filename, filename, temp_filepath = save_temp_image(file)
        verification_status, hash_object, ref_filepath = self_verify_image(temp_filepath)
        print(f"Verification status: {verification_status}.")

        if verification_status == config.VERIFICATION_STATUS["ACCEPTED"]:
            perm_filepath = save_webp_image(temp_filepath)
            await save_uploaded_data_to_db(user_uid, original_filename, filename, temp_filepath, signature, verification_status, hash_object)
            return {"message": f"Image {original_filename} registered successfully."}
        elif verification_status == config.VERIFICATION_STATUS["PENDING"]:
            perm_filepath = save_webp_image(temp_filepath)
            await save_uploaded_data_to_db(user_uid, original_filename, filename, perm_filepath, signature, verification_status, hash_object)
            return {"message": f"Image {original_filename} is under consideration."}
        else:
            return {"message": f"Image {original_filename} is rejected. A reference image can be found at {ref_filepath}."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# @router.post("/key")
# async def upload_key(request: RequestUploadPublicKey):    
#     user_uid = request.state.user['uid']                                    # Access the user UID from Firebase token
#     certi_url = request.certi_url
#     issuer_name = request.issuer_name
#     not_before = request.not_before
#     not_after = request.not_after
#     status = request.status
#     public_key = request.public_key
#     print(f"Public key {public_key[:10]}...{public_key[-10:]} received from user {user_uid}.")
    
#     try:
#         insert_key_certi(user_uid, certi_url, issuer_name, not_before, not_after, status, public_key)
#         return {"message": "Public key registered successfully."}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# # the image is not of File type anymore, now it is sent with base64 encoding from the frontend
# @router.post("/image/base64")
# async def upload_image_base64(userUID: int = Form(...), image: str = Form(...)):

#     userUID = 2
#     print(f"Base64 string received from user {userUID}.")
#     try: 
#         filepath = os.path.join(config.TEMP_IMAGE_DIR, "temp.jpg")
#         with open(filepath, "wb") as buffer:
#             buffer.write(image)
#         buffer.close()
#         verification_status, hash_object, ref_filepath = self_verify_image(filepath)
#         print(f"Verification status: {verification_status}.")

#         if verification_status == config.VERIFICATION_STATUS["ACCEPTED"]:
#             save_uploaded_data_to_db(userUID, filepath, verification_status, hash_object)
#             # TODO: prompt user to select private key file, next request only need to send the signature
#             return {"message": "Image registered successfully. Please sign the image."}
#         elif verification_status == config.VERIFICATION_STATUS["PENDING"]:
#             save_uploaded_data_to_db(userUID, filepath, verification_status, hash_object)
#             return {"message": "Image is under consideration."}
#         else:
#             return {"message": f"Image is rejected. A reference image can be found at {ref_filepath}."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# def extract_metadata_from_base64(filepath: str):

#     # read base64 string from filepath (txt)
#     with open(filepath, "r") as f:
#         base64_str = f.read()
    
#     # Add padding if necessary
#     missing_padding = len(base64_str) % 4
#     if missing_padding:
#         base64_str += '=' * (4 - missing_padding)

#     # decode base64 string to image data
#     image_data = base64.b64decode(base64_str)

#     # save image data to image file
#     extension = base64_str.split("/")[1].split(";")[0]
#     image_path = filepath.replace(".txt", f".{extension}")
#     with open(image_path, 'wb') as image_file:
#         image_file.write(image_data)   
    
#     # extract metadata from image file
#     metadata = extract_metadata(image_path)
#     return metadata


# if __name__ == "__main__":
#     metadata = extract_metadata_from_base64("/home/pc/imagecert/backend/data/images/pictureforQuan.txt")
#     print(metadata)



