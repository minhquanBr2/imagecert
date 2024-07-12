from db.db_insert import insert_image, insert_hash, insert_verification_status
from internal.upload.extract_metadata import extract_metadata
import time

def save_image(userUID, filepath):
    metadata = extract_metadata(filepath)
    # try if timestamp exists, else assign ""
    # TODO: mapping metadata to db schema
    timestamp = metadata.get("DateTime", "")
    caption = metadata.get("ImageDescription", "")
    location = metadata.get("GPSInfo", "")
    deviceName = metadata.get("Model", "")
    signature = ""
    imageID = insert_image(userUID, filepath, timestamp, caption, location, deviceName, signature)
    return imageID


def save_hash(imageID, hash):
    insert_hash(imageID, hash["type"], hash["value"])
    

def save_verification_status(imageID, result, verificationTimestamp):
    insert_verification_status(imageID, 0, result, verificationTimestamp)


def save_uploaded_data_to_db(userUID, filepath, verification_status, hash):
    imageID = save_image(userUID, filepath)
    save_hash(imageID, hash)
    save_verification_status(imageID, verification_status, time.time())