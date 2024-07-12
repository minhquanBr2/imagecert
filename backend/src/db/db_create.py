import db_connect


def create_table_image():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image (
            imageID INTEGER PRIMARY KEY AUTOINCREMENT,
            userUID INTEGER NOT NULL,
            url TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            caption TEXT,
            location TEXT,
            deviceName TEXT,
            signature TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def create_table_hash():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hash (
            hashID INTEGER PRIMARY KEY AUTOINCREMENT,
            imageID INTEGER NOT NULL,
            type TEXT NOT NULL,
            value TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def create_table_verification_status():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verificationStatus (
            statusID INTEGER PRIMARY KEY AUTOINCREMENT,
            imageID INTEGER NOT NULL,
            adminUID INTEGER NOT NULL,
            result INTEGER NOT NULL,
            verificationTimestamp TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table_image()
    create_table_hash()
    create_table_verification_status()