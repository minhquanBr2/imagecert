from pydantic import BaseModel
from schemas import options_schemas

class RequestUploadImage(BaseModel):
    signature: str

    class Config:
        json_schema_extra = {
            "example": {
                "signature": "abcxyz"
            }
        }


class RequestVerifyImage(BaseModel):
    image_id: int
    admin_uid: int
    result: options_schemas.AdminVerificationResultOptions

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": 1,
                "admin_uid": 1,
                "result": 0
            }
        }