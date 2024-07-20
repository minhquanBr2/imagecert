import datetime
import config
import requests


def get_original_filename(image_id):
    url = f"{config.DB_ENDPOINT_URL}/select/image/original/{image_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    results = response.json()["message"]
    if len(results) == 0:
        return None

    return results[0][0]


def verify_image(image_id, admin_uid, result):
    original_filename = get_original_filename(image_id)
    if original_filename == None:
        return {"message": f"Image {image_id} not found."}
    
    data = {
        "image_id": image_id,
        "admin_uid": admin_uid,
        "result": result,
        "verification_timestamp": datetime.datetime().now().isoformat()
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/verification_status"
    response = requests.post(url, data)
    if response.status_code != 200:
        return {"message": f"Error saving verification status for image {image_id}."}    

    if result == config.VERIFICATION_STATUS["ACCEPTED"]:
        return {"message": f"Image {original_filename} registered successfully. Please sign the image."}
    else:
        return {"message": f"Image {original_filename} is rejected."}