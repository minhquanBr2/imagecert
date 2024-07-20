import sqlite3
import config


def select_image(imageID, attributes: list):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''SELECT {','.join(attributes)} FROM image WHERE imageID = {imageID}'''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results
