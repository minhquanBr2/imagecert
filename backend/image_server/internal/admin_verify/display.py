import sqlite3
import config
import os

def get_pending_images():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT image.imageID, image.filename FROM image JOIN verificationStatus ON image.imageID = verificationStatus.imageID WHERE verificationStatus.result = 1'
    cursor.execute(query)
    image_filenames = cursor.fetchall()

    response = []
    for filename in image_filenames:
        response.append({
            "imageID": filename[0],
            "filename": os.path.join(config.IMAGE_DISPLAY_URL, f"{filename[1]}.webp")
        })

    conn.commit()
    conn.close()
    return response