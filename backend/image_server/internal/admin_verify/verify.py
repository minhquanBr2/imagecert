from db.db_insert import insert_verification_status
from db.db_select import select_image
import datetime
import config


def get_original_filename(image_id):
    return select_image(image_id, ["originalFilename"])[0][0]


def verify_image(image_id, admin_uid, result):
    original_filename = get_original_filename(image_id)
    insert_verification_status(image_id, admin_uid, result, datetime.datetime().now().timestamp())
    if result == config.VERIFICATION_STATUS["ACCEPTED"]:
        return {"message": f"Image {original_filename} registered successfully. Please sign the image."}
    else:
        return {"message": f"Image {original_filename} is rejected."}