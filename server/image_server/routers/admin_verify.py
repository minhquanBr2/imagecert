from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from internal.admin_verify import display, verify
from internal.utils import getEmailFromUid, getUserUidFromImageID
from schemas.request_schemas import RequestVerifyImage
import config
import requests

router = APIRouter(
    prefix = '/admin_verify',
    tags = ['admin_verify'],
)


@router.get("/get_pendings")
async def get_pending_images():
    url = f"{config.DB_ENDPOINT_URL}/select/pending_images"
    response = requests.get(url)
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.get("/verification_history/{admin_uid}")
async def get_verification_history(admin_uid: str):
    response = await display.get_verification_history(admin_uid)
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.post("/verify")
async def verify_image(request: RequestVerifyImage):
    print(f"Request from admin: {request}")
    try:
        image_id = request.image_id
        admin_uid = request.admin_uid
        result = config.VERIFICATION_STATUS_FE_BE_MAPPING[request.result]
        print(f"Verification request received from admin {admin_uid}.")
        status_code, data = await verify.verify_image(image_id, admin_uid, result)
        return JSONResponse(status_code=status_code, content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Internal server error: {str(e)}"})


@router.get("/email/{user_uid}")
async def get_email_by_user_uid(user_uid: str):
    data = getEmailFromUid.get_user_email_by_uid(user_uid)
    return JSONResponse(status_code=200, content=data)