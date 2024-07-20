import sqlite3
import sys
sys.path.append('..')
import config

def connect_db(db_name=config.IMAGEDB_PATH):
    return sqlite3.connect(db_name)
