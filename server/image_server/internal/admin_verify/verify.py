import datetime
import config
import requests
import sys
sys.path.append("..")
from internal.email_send.sendEmail import send_email_with_template
from internal.email_send.constant import pass_template, fail_template, subject, sender_email, sender_password
from internal.utils.getEmailFromUid import get_user_email_by_uid
from internal.upload.save import save_verification_status
from internal.utils.getUserUidFromImageID import get_user_uid_from_image_id

def get_original_filename(image_id: str):
    url = f"{config.DB_ENDPOINT_URL}/select/image/original/{image_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    results = response.json()["message"]
    if len(results) == 0:
        return None

    return results[0][0]

async def verify_image(image_id: int, admin_uid: str, result: int):
    try:
        original_filename = get_original_filename(image_id)
        if original_filename is None:
            raise ValueError(f"Image {image_id} not found.")

        user_uid = await get_user_uid_from_image_id(image_id)
        print(f"User UID: {user_uid}")
        if user_uid is None:
            raise ValueError(f"User UID not found for image {image_id}.")

        user_email = get_user_email_by_uid(user_uid)
        if user_email == 'x':
            raise ValueError(f"User email not found for user {user_uid}.")

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        response = await save_verification_status(image_id,admin_uid, result, timestamp)
        if response.status_code != 200:
            raise RuntimeError(f"Error saving verification status for image {image_id}.")
        
        if result == config.VERIFICATION_STATUS["ACCEPTED"]:
            # Send email indicating verification passed
            send_email_with_template(pass_template, config.CLIENT_APP_USER, user_email, subject, sender_email, sender_password)
            return {"message": f"Image {original_filename} registered successfully."}
        else:
            # Send email indicating verification failed
            send_email_with_template(fail_template, config.MAIL_COMPOSE_URL, user_email, subject, sender_email, sender_password)
            return {"message": f"Image {original_filename} is rejected."}

    except Exception as e:
        print(f"Error verifying image: {str(e)}")
        return {"message": f"Error verifying image: {str(e)}"}

