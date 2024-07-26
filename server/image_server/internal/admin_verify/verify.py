import datetime
import config
import requests
import sys
sys.path.append("..")
from internal.email_send.sendEmail import send_email_with_template
from internal.email_send.constant import pass_template, fail_template, subject, sender_email, sender_password
from internal.utils.getEmailFromUid import get_user_email_by_uid
from internal.upload.save import save_verification_status


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
    original_filename = get_original_filename(image_id)
    if original_filename == None:
        return {"message": f"Image {image_id} not found."}    
    
    timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
    response = await save_verification_status(image_id, admin_uid, result, timestamp)
    if response.status_code != 200:
        return {"message": f"Error saving verification status for image {image_id}."}    

    user_uid = get_user_uid_from_image_id(image_id)
    if user_uid == None:
        return {"message": f"User UID not found for image {image_id}."}    

    if result == config.VERIFICATION_STATUS["ACCEPTED"]:
        # SEND EMAIL PASS HERE
        send_email_with_template(pass_template, "http://localhost:3000", get_user_email_by_uid(user_uid), subject, sender_email, sender_password)
        return {"message": f"Image {original_filename} registered successfully. Please sign the image."}
    else:
        # SEND EMAIL FAIL HERE
        send_email_with_template(fail_template, "http://localhost:3000", get_user_email_by_uid(user_uid), subject, sender_email, sender_password)
        return {"message": f"Image {original_filename} is rejected."}