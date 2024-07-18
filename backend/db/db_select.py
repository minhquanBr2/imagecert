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


def select_key_certi_from_user_uid(user_uid):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''SELECT * FROM keyCerti WHERE userUID = {user_uid}'''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    if len(results) == 0:
        return None
    else:
        return {
            "user_uid": results[0][1],
            "certi_url": results[0][2],
            "issuer_name": results[0][3],
            "not_before": results[0][4],
            "not_after": results[0][5],
            "status": results[0][6],
            "public_key": results[0][7]
        }
