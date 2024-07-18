from pydantic import BaseModel


class RequestUploadPublicKeyCerti(BaseModel):
    user_uid: str
    certi_url: str
    issuer_name: str
    not_before: str 
    not_after: str
    status: str
    public_key: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_uid": "123456",
                "certi_url": "https://example.com",
                "issuer_name": "John Doe",
                "not_before": "2021-01-01",
                "not_after": "2022-01-01",
                "status": "0",
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