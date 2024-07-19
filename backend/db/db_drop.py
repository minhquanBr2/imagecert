import db_connect


def drop_table_key_certi():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS keyCerti;
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    drop_table_key_certi()