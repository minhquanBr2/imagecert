from internal.upload.extract_metadata import extract_metadata
from internal.upload.preprocess import generate_image_name
import datetime
import cv2
import os
import config
import requests


async def save_image(userUID, originalFilename, filename, timestamp, temp_filepath, signature, ref_filepath):
    metadata = extract_metadata(temp_filepath)
    payload = {
        "user_uid": userUID,
        "original_filename": originalFilename,
        "filename": filename,
        "timestamp": timestamp,
        "caption": metadata.get("ImageDescription", ""),
        "location": metadata.get("GPSInfo", ""),
        "device_name": metadata.get("Model", ""),
        "signature": signature,
        "ref_filepath": ref_filepath
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/image"
    response = requests.post(url, json = payload)
    if response.status_code == 200:
        print(f"Image {originalFilename} saved to db with new file name as {filename}.")
        return int(response.json()["message"]["image_id"])
    return None


async def save_hash(imageID, hash):
    payload = {
        "image_id": imageID,
        "hash_type": hash["type"],
        "value": hash["value"]
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/hash"
    response = requests.post(url, json = payload)
    if response.status_code != 200:
        print(f"Error saving hash for image with ID {imageID}.")
    else:
        print(f"Hash saved for image with ID {imageID}.")
    

async def save_verification_status(imageID, result, verificationTimestamp):
    payload = {
        "image_id": imageID,
        "admin_uid": "",
        "result": result,
        "verification_timestamp": verificationTimestamp
    }
    url = f"{config.DB_ENDPOINT_URL}/insert/verification_status"
    response = requests.post(url, json = payload)
    return response


async def save_refs(imageID, refImageIDs):
    for refImageID in refImageIDs:
        payload = {
            "image_id": imageID,
            "ref_image_id": refImageID
        }
        url = f"{config.DB_ENDPOINT_URL}/insert/ref"
        response = requests.post(url, json = payload)
        if response.status_code != 200:
            print(f"Error saving reference image for image with ID {imageID}.")
        else:
            print(f"Reference image saved for image with ID {imageID}.")


async def save_uploaded_data_to_db(userUID, originalFilename, filename, temp_filepath, signature, verificationStatus, hash, refImageIDs):
    timestamp = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S.%f')
    imageID = await save_image(userUID, originalFilename, filename, timestamp, temp_filepath, signature, "dummy_filepath")
    print(f"Image ID: {imageID}")
    await save_hash(imageID, hash)
    await save_verification_status(imageID, verificationStatus, timestamp)
    await save_refs(imageID, refImageIDs)


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