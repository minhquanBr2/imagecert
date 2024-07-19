from fastapi import APIRouter, HTTPException, Request
from internal.admin_verify import display, verify
from schemas.request_schemas import RequestVerifyImage
import os

router = APIRouter(
    prefix = '/admin_verify',
    tags = ['admin_verify'],
)


@router.get("/get_pendings")
async def get_pending_images():
    return display.get_pending_images()


@router.post("/verify")
async def verify_image(req: Request, request: RequestVerifyImage):
    admin_uid = req.state.user['uid']                                    # Access the user UID from Firebase token
    print(f"Verification request received from admin {admin_uid}.")

    try:
        image_id = request.image_id
        result = request.result
        verify.verify_image(image_id, admin_uid, result)
        return {"message": "Image verification status updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")