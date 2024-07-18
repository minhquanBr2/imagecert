import sqlite3
import sys
sys.path.append('..')
import config

def test_image():
    print("\nTesting image table")
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM image'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()
    print()


def test_hash():
    print("\nTesting hash table")
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM hash'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()
    print()


def test_verification_status():
    print("\nTesting verification_status table")
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM verificationStatus'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()
    print()


def test_key_certi():
    print("\nTesting key_certi table")
    conn = sqlite3.connect(config.IMAGEDB_PATH)
    cursor = conn.cursor()
    query = 'SELECT * FROM keyCerti'
    cursor.execute(query)
    # print the result
    for row in cursor.fetchall():
        print(row)
    conn.commit()
    conn.close()
    print()


if __name__ == "__main__":
    test_image()   
    test_hash()
    test_verification_status()
    test_key_certi()