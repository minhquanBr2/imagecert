from fastapi import APIRouter, HTTPException, Request, Depends
from internal.admin_verify import display, verify
from schemas.request_schemas import RequestVerifyImage
import config
from internal.utils import getEmailFromUid, getUserUidFromImageID
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix = '/admin_verify',
    tags = ['admin_verify'],
)


@router.get("/get_pendings")
async def get_pending_images():
    results = await display.get_pending_images()
    return results



@router.get("/verification_history/{admin_uid}")
async def get_verification_history(admin_uid: str):
    results = await display.get_verification_history(admin_uid)
    return results


@router.post("/verify")
async def verify_image(request: RequestVerifyImage):
    print(f"Request from admin: {request}")
    try:
        image_id = request.image_id
        admin_uid = request.admin_uid
        result = config.VERIFICATION_STATUS_FE_BE_MAPPING[request.result]
        print(f"Verification request received from admin {admin_uid}.")
        response = await verify.verify_image(image_id, admin_uid, result)
        print('response:', response)
        if "Error" in response.get("message", ""):
            raise RuntimeError(response["message"])
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/email/{user_uid}")
async def get_email_by_user_uid(user_uid: str):
    results = getEmailFromUid.get_user_email_by_uid(user_uid)
    return results