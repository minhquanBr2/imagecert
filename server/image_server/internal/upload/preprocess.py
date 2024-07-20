import datetime
import hashlib

def generate_image_name():
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    hash_object = hashlib.sha256(timestamp.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest
