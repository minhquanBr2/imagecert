import sqlite3
import config
import os


def standardize_timestamp(timestamp):
    if ":" in timestamp:
        return timestamp
    return f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[8:10]}:{timestamp[10:12]}:{timestamp[12:14]}.{timestamp[14:]}"


def select_image(imageID, attributes: list) -> list:
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''SELECT {','.join(attributes)} FROM image WHERE imageID = {imageID}'''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def select_all_accepted_hashes() -> list:
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = '''
            SELECT hash.imageID, hash.value
            FROM hash
            JOIN verificationStatus on hash.imageID = verificationStatus.imageID
            WHERE verificationStatus.result = 0
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


async def select_all_key_certis_from_user_uid(user_uid) -> list:
    
    # print all tables
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    for table in tables:
        print(table[0])
    conn.commit()
    conn.close()

    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''SELECT * FROM keyCerti WHERE userUID = '{user_uid}' ORDER BY certiID DESC'''
    cursor.execute(query)
    records = cursor.fetchall()
    conn.commit()
    conn.close()

    print("Results length: ", len(records))
    if len(records) == 0:
        return None
    else:
        results = []
        for record in records:
            results.append({
                "certi_id": record[0],
                "user_uid": record[1],
                "certi": record[2],
                "issuer_name": record[3],
                "not_before": record[4],
                "not_after": record[5],
                "status": record[6],
                "public_key": record[7]
            })
        return results


# def select_curr_key_certi_from_user_uid(user_uid):
#     conn = sqlite3.connect(config.IMAGEDB_PATH)
#     cursor = conn.cursor()
#     query = f'''SELECT * FROM keyCerti WHERE userUID = {user_uid} AND status = 1'''
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.commit()
#     conn.close()

#     if len(results) == 0:
#         return None
#     else:
#         return {
#             "user_uid": results[0][1],
#             "certi": results[0][2],
#             "issuer_name": results[0][3],
#             "not_before": results[0][4],
#             "not_after": results[0][5],
#             "status": results[0][6],
#             "public_key": results[0][7]
#         }


def select_verification_history(admin_uid) -> list:
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''
            SELECT filename, result, verificationTimestamp 
            FROM verificationStatus 
            JOIN image on image.imageID = verificationStatus.imageID
            WHERE adminUID = '{admin_uid}'
            '''
    print("Query:", query)
    cursor.execute(query)
    records = cursor.fetchall()
    conn.commit()
    conn.close()    
    
    results = []
    for record in records:
        results.append({
            "imageURL": os.path.join(config.IMAGE_DISPLAY_URL, f"{record[0]}.webp"),
            "result": record[1],
            "verificationTimestamp": standardize_timestamp(record[2])
        })
    return results


def select_pending_images() -> list:
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = '''
            SELECT image.imageID, image.filename, ref_image.filename
            FROM image 
            JOIN verificationStatus ON image.imageID = verificationStatus.imageID 
            JOIN ref ON image.imageID = ref.imageID
            JOIN image AS ref_image ON ref.refImageID = ref_image.imageID
            GROUP BY image.imageID
            HAVING COUNT(*) = SUM(verificationStatus.result)
            '''
    cursor.execute(query)
    images = cursor.fetchall()
    conn.commit()
    conn.close()

    results = []
    temp_results = {}
    for image in images:
        key = image[0]
        ref_filepath = os.path.join(config.IMAGE_DISPLAY_URL, f"{image[2]}.webp")
        if key not in temp_results:
            temp_results[key] = {"imageID": image[0], "imageURL": os.path.join(config.IMAGE_DISPLAY_URL, f"{image[1]}.webp"), "refFilepaths": [ref_filepath]}
        else:
            temp_results[key]["refFilepaths"].append(ref_filepath)
    for key in temp_results.keys():
        results.append(temp_results[key])
    return results


def select_all_images() -> list:
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = '''
            SELECT image.imageID, image.filename, image.userUID, image.timestamp
            FROM image 
            JOIN verificationStatus ON image.imageID = verificationStatus.imageID 
            WHERE verificationStatus.result = 0
            ORDER BY image.imageID DESC
            '''
    cursor.execute(query)
    images = cursor.fetchall()
    conn.commit()
    conn.close()

    results = []
    print(f"Images: {images}")
    for image in images:
        results.append({
            "imageID": image[0],
            "imageURL": os.path.join(config.IMAGE_DISPLAY_URL, f"{image[1]}.webp"),
            "userUID": image[2],
            "timestamp": image[3]
        })

    if len(results) >= 1:
        print(f"First image: {results[0]['imageURL']}")
    return results


def select_user_uid_from_image_id(image_id: int):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = f'''SELECT userUID FROM image WHERE imageID = {image_id}'''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    if len(results) == 0:
        return None
    else:
        return results[0][0]
    