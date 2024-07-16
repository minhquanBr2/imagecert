from db.db_insert import insert_image, insert_hash, insert_verification_status
from internal.upload.extract_metadata import extract_metadata
import time
import cv2
import os
import config

def save_image(userUID, originalFilename, filename, temp_filepath):
    metadata = extract_metadata(temp_filepath)
    # try if timestamp exists, else assign ""
    # TODO: mapping metadata to db schema
    timestamp = metadata.get("DateTime", "")
    caption = metadata.get("ImageDescription", "")
    location = metadata.get("GPSInfo", "")
    deviceName = metadata.get("Model", "")
    signature = ""
    imageID = insert_image(userUID, originalFilename, filename, timestamp, caption, location, deviceName, signature)
    return imageID


def save_hash(imageID, hash):
    insert_hash(imageID, hash["type"], hash["value"])
    

def save_verification_status(imageID, result, verificationTimestamp):
    insert_verification_status(imageID, 0, result, verificationTimestamp)


def save_uploaded_data_to_db(userUID, originalFilename, filename, temp_filepath, verificationStatus, hash):
    imageID = save_image(userUID, originalFilename, filename, temp_filepath)
    save_hash(imageID, hash)
    save_verification_status(imageID, verificationStatus, time.time())


def save_webp_image(filepath):
    filename = filepath.split("/")[-1]
    webp_filename = filename.replace(filename.split(".")[-1], "webp")
    webp_filepath = os.path.join(config.PERM_IMAGE_DIR, webp_filename)
    img = cv2.imread(filepath)
    cv2.imwrite(webp_filepath, img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
    return webp_filepath


def save_temp_image(filepath):
    pass