from pydantic import BaseModel


class RequestUploadImage(BaseModel):
    user_uid: str
    original_filename: str
    filename: str
    timestamp: str
    caption: str
    location: str
    device_name: str
    signature: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_uid": "123456",
                "original_filename": "image.jpg",
                "filename": "cb0ewf0jpwvane2bsamr0nq.jpg",
                "timestamp": "2021-01-01T00:00:00",
                "caption": "A beautiful image",
                "location": "Earth",
                "device_name": "iPhone",
                "signature": "abcxyz"
            }
        }


class RequestUploadHash(BaseModel):
    image_id: int
    hash_type: str
    value: str

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": 1,
                "hash_type": "SHA256",
                "value": "abcxyz"
            }
        }


class RequestUploadVerificationStatus(BaseModel):
    image_id: int
    admin_uid: str
    result: int
    verification_timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": 1,
                "admin_uid": "123456",
                "result": 1,
                "verification_timestamp": "2021-01-01T00:00:00"
            }
        }


class RequestUploadPublicKeyCerti(BaseModel):
    user_uid: str
    certi: str
    issuer_name: str
    not_before: str 
    not_after: str
    status: int
    public_key: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_uid": "123456",
                "certi": "---BEGIN CERTIFICATE---\nabcxyz\n---END CERTIFICATE---",
                "issuer_name": "John Doe",
                "not_before": "2021-01-01",
                "not_after": "2022-01-01",
                "status": 1,
                "public_key": "abcxyz"
            }
        }


class RequestRetrievePublicKeyCerti(BaseModel):
    user_uid: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_uid": "123456"
            }
        }


class RequestRetrieveImage(BaseModel):
    image_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": 1
            }
        }