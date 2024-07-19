import sqlite3
import config

def insert_image(userUID, originalFilename, filename, timestamp, caption, location, deviceName, signature):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO image (userUID, originalFilename, filename, timestamp, caption, location, deviceName, signature)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (userUID, originalFilename, filename, timestamp, caption, location, deviceName, signature))
    conn.commit()
    conn.close()
    return cursor.lastrowid


def insert_hash(imageID, type, value):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hash (imageID, type, value)
        VALUES (?, ?, ?)
    ''', (imageID, type, value))
    conn.commit()
    conn.close()


def insert_verification_status(imageID, adminUID, result, verificationTimestamp):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO verificationStatus (imageID, adminUID, result, verificationTimestamp)
        VALUES (?, ?, ?, ?)
    ''', (imageID, adminUID, result, verificationTimestamp))
    conn.commit()
    conn.close()


def insert_key_certi(userUID, certiURL, issuerName, notBefore, notAfter, status, publicKey):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO keyCerti (userUID, certiURL, issuerName, notBefore, notAfter, status, publicKey)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (userUID, certiURL, issuerName, notBefore, notAfter, status, publicKey))
    conn.commit()
    conn.close()