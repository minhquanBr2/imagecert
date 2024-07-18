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


class RequestUploadPublicKey(BaseModel):
    certi_url: str
    issuer_name: str
    not_before: str 
    not_after: str
    status: str
    public_key: str

    class Config:
        json_schema_extra = {
            "example": {
                "certi_url": "https://example.com",
                "issuer_name": "John Doe",
                "not_before": "2021-01-01",
                "not_after": "2022-01-01",
                "status": "0",
                "public_key": "abcxyz"
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
