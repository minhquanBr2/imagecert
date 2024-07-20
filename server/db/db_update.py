import sqlite3
import config


def update_image(imageID, attributes: list, values: list):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE image SET '
    for i in range(len(attributes)):
        query += attributes[i] + ' = ?'
        if i != len(attributes) - 1:
            query += ', '
    query += ' WHERE imageID = ?'
    values.append(imageID)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def update_hash(hashID, attributes: list, values: list):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE hash SET '
    for i in range(len(attributes)):
        query += attributes[i] + ' = ?'
        if i != len(attributes) - 1:
            query += ', '
    query += ' WHERE hashID = ?'
    values.append(hashID)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def update_verification_status(statusID, attributes: list, values: list):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE verificationStatus SET '
    for i in range(len(attributes)):
        query += attributes[i] + ' = ?'
        if i != len(attributes) - 1:
            query += ', '
    query += ' WHERE statusID = ?'
    values.append(statusID)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def update_key_certi(certiID, attributes: list, values: list):
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE keyCerti SET '
    for i in range(len(attributes)):
        query += attributes[i] + ' = ?'
        if i != len(attributes) - 1:
            query += ', '
    query += ' WHERE certiID = ?'
    values.append(certiID)
    cursor.execute(query, values)
    conn.commit()
    conn.close()