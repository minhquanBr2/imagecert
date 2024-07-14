import sqlite3
import sys
sys.path.append('..')
import config

def test_image():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM image'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()


def test_hash():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM hash'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()


def test_verification_status():
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM verificationStatus'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # test_image()   
    # test_hash()
    test_verification_status()