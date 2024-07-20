import db_connect


# role = 0: user
# role = 1: admin
def create_table_user():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            userUID TEXT PRIMARY KEY,
            publicKey TEXT NOT NULL,
            role INTEGER NOT NULL       
        );
    ''')
    conn.commit()
    conn.close()


def create_table_image():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image (
            imageID INTEGER PRIMARY KEY AUTOINCREMENT,
            userUID INTEGER NOT NULL,
            originalFilename TEXT NOT NULL,
            filename TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            caption TEXT,
            location TEXT,
            deviceName TEXT,
            signature TEXT NOT NULL,
            ref_filepath TEXT
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
            imageID TEXT NOT NULL,
            adminUID TEXT NOT NULL,
            result INTEGER NOT NULL,
            verificationTimestamp TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def create_table_image_certi():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imageCerti (
            certiID INTEGER PRIMARY KEY AUTOINCREMENT,
            userUID INTEGER NOT NULL,
            imageID INTEGER NOT NULL,
            certiURL TEXT NOT NULL,
            issuerName TEXT NOT NULL,
            notBefore TEXT NOT NULL,
            notAfter TEXT NOT NULL,
            status INT NOT NULL,
            signature TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def create_table_key_certi():
    conn = db_connect.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyCerti (
            certiID INTEGER PRIMARY KEY AUTOINCREMENT,
            userUID INTEGER NOT NULL,
            certi TEXT NOT NULL,
            issuerName TEXT NOT NULL,
            notBefore TEXT NOT NULL,
            notAfter TEXT NOT NULL,
            status INT NOT NULL,
            publicKey TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_table_user()
    create_table_image()
    # create_table_hash()
    # create_table_verification_status()
    # create_table_image_certi()
    # create_table_key_certi()