import datetime
import config
import requests
import json
import os
import sys
sys.path.append("..")
from internal.email_send.sendEmail import send_email_with_template
from internal.utils.getEmailFromUid import get_user_email_by_uid
from internal.upload.save import save_verification_status
from fastapi.responses import JSONResponse


EMAIL_CONSTANTS_PATH = os.getenv('EMAIL_CONSTANTS_PATH')
with open(EMAIL_CONSTANTS_PATH, 'r') as f:
    email_data = json.load(f)
    pass_template = email_data["pass_template"]
    fail_template = email_data["fail_template"]
    subject = email_data["subject"]
    sender_email = email_data["sender_email"]
    sender_password = email_data["sender_password"]


async def get_original_filename(image_id: str):
    url = f"{config.DB_ENDPOINT_URL}/select/image/original/{image_id}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        return result[0][0]
    return None

async def get_user_uid_from_image_id(image_id: str):
    url = f"{config.DB_ENDPOINT_URL}/select/image/{image_id}/user_uid"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        return result
    return None

async def verify_image(image_id: int, admin_uid: str, result: int):
    try:
        original_filename = await get_original_filename(image_id)
        print(f"Original filename: {original_filename}")
        if original_filename is None:
            return 500, {"message": f"Image {image_id} not found."}

        user_uid = await get_user_uid_from_image_id(image_id)
        print(f"User UID: {user_uid}")
        if user_uid is None:
            return 500, {"message": f"Image {image_id} not found."}

        user_email = get_user_email_by_uid(user_uid)
        print(f"User email: {user_email}")
        if user_email == '' or user_email == None:
            return 500, {"message": f"User email not found for user {user_uid}."}

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        response = await save_verification_status(image_id, admin_uid, result, timestamp)
        print(f"Verification timestamp at admin: {timestamp}")
        if response.status_code != 200:
            return 500, {"message": f"Error saving verification status for image {image_id}."}
        
        if result == config.VERIFICATION_STATUS["ACCEPTED"]:
            # Send email indicating verification passed
            send_email_with_template(pass_template, config.CLIENT_APP_USER, user_email, subject, sender_email, sender_password)
            return 200, {"message": f"Image {original_filename} registered successfully."}
        else:
            # Send email indicating verification failed
            send_email_with_template(fail_template, config.MAIL_COMPOSE_URL, user_email, subject, sender_email, sender_password)
            return 200, {"message": f"Image {original_filename} is rejected."}

    except Exception as e:
        print(f"Error verifying image: {str(e)}")
        return 500, {"message": f"Error verifying image: {str(e)}"}

