import sqlite3
import config
import os


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
            "certi": results[0][2],
            "issuer_name": results[0][3],
            "not_before": results[0][4],
            "not_after": results[0][5],
            "status": results[0][6],
            "public_key": results[0][7]
        }


def select_verification_history(admin_uid):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f"SELECT * FROM verificationStatus WHERE adminUID = '{admin_uid}'"
    print("Query:", query)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def select_pending_images():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = '''
            SELECT image.imageID, image.filename 
            FROM image 
            JOIN verificationStatus ON image.imageID = verificationStatus.imageID 
            GROUP BY image.imageID
            HAVING COUNT(*) = SUM(verificationStatus.result)
            '''
    cursor.execute(query)
    image_filenames = cursor.fetchall()
    conn.commit()
    conn.close()

    results = []
    for filename in image_filenames:
        results.append({
            "imageID": filename[0],
            "filename": os.path.join(config.IMAGE_DISPLAY_URL, f"{filename[1]}.webp")
        })

    # print("Results:", results)
    return results



    

    