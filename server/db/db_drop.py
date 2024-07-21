import db_connect


def drop_table_key_certi():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS keyCerti;
    ''')
    conn.commit()
    conn.close()


def drop_table_verification_status():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS verificationStatus;
    ''')
    conn.commit()
    conn.close()


def drop_table_image():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS image;
    ''')
    conn.commit()
    conn.close()



if __name__ == "__main__":
    drop_table_key_certi()
    # drop_table_verification_status()
    # drop_table_image()