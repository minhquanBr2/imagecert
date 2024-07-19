from pydantic import BaseModel


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