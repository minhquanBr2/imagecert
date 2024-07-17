from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from internal.admin_verify import display
import os

router = APIRouter(
    prefix = '/admin_verify',
    tags = ['admin_verify'],
)

@router.get("/get_pendings")
async def get_pending_images():
    image_urls = display.get_pending_images()
    return {"image_urls": image_urls}
