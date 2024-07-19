from internal.upload.extract_metadata import extract_metadata
from internal.upload.preprocess import generate_image_name
import time
import cv2
import os
import config
import requests


def save_image(userUID, originalFilename, filename, temp_filepath, signature):
    metadata = extract_metadata(temp_filepath)
    data = {
        "user_uid": userUID,
        "original_filename": originalFilename,
        "filename": filename,
        "timestamp": metadata.get("DateTime", ""),
        "caption": metadata.get("ImageDescription", ""),
        "location": metadata.get("GPSInfo", ""),
        "device_name": metadata.get("Model", ""),
        "signature": signature
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/image"
    response = requests.post(url, data)
    if response.status_code == 200:
        return response.json()["message"]["image_id"]
    return None


def save_hash(imageID, hash):
    data = {
        "image_id": imageID,
        "hash_type": hash["type"],
        "value": hash["value"]
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/hash"
    response = requests.post(url, data)
    if response.status_code != 200:
        print(f"Error saving hash for image {imageID}.")
        return None
    

def save_verification_status(imageID, result, verificationTimestamp):
    data = {
        "image_id": imageID,
        "admin_uid": "",
        "result": result,
        "verification_timestamp": verificationTimestamp
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/verification_status"
    response = requests.post(url, data)
    if response.status_code != 200:
        print(f"Error saving verification status for image {imageID}.")
        return None


def save_uploaded_data_to_db(userUID, originalFilename, filename, temp_filepath, signature, verificationStatus, hash):
    imageID = save_image(userUID, originalFilename, filename, temp_filepath, signature)
    save_hash(imageID, hash)
    save_verification_status(imageID, verificationStatus, time.time())


def save_webp_image(filepath):
    filename = filepath.split("/")[-1]
    webp_filename = filename.replace(filename.split(".")[-1], "webp")
    webp_filepath = os.path.join(config.PERM_IMAGE_DIR, webp_filename)
    img = cv2.imread(filepath)
    cv2.imwrite(webp_filepath, img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
    return webp_filepath


def save_temp_image(file):
    original_filename = file.filename
    extension = original_filename.split(".")[-1]
    filename = generate_image_name()
    temp_filepath = os.path.join(config.TEMP_IMAGE_DIR, f"{filename}.{extension}")

    with open(temp_filepath, "wb") as buffer:
        buffer.write(file.file.read())
    file.file.close()
    
    return original_filename, filename, temp_filepath