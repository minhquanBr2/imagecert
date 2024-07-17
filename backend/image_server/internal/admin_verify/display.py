import sqlite3
import config
import os

def get_pending_images():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT image.filename FROM image JOIN verificationStatus ON image.imageID = verificationStatus.imageID WHERE verificationStatus.result = 1'
    cursor.execute(query)
    image_filenames = cursor.fetchall()
    image_urls = [os.path.join(config.IMAGE_DISPLAY_URL, f"{filename[0]}.webp") for filename in image_filenames]
    conn.commit()
    conn.close()
    return image_urls