import config
from tndrlib import common as log
from tndrlib import createdb, create_matchdb

import os
import sqlite3

def conn_authdb():
    db_path = config.store_settings['adb_path']
    if not db_path:
        raise Exception('Path authdb is empty. See config')	

    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    
    conn = None
    if os.path.exists(db_path):

        log.log_info(f'Connect cache db {db_path}')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

    else:
        log.log_info(f'Create bot db {db_path}')

        conn, cursor = createdb.create_db()
    
    return conn, cursor

def conn_matchdb():
    mdb_path = config.store_settings['mdb_path']
    if not mdb_path:
        raise Exception('Path matchdb is empty. See config')

    if not os.path.exists(os.path.dirname(mdb_path)):
        os.makedirs(os.path.dirname(mdb_path))
    
    conn = None
    if os.path.exists(mdb_path):

        log.log_info(f'Connect cache db {mdb_path}')

        conn = sqlite3.connect(mdb_path)
        cursor = conn.cursor()

    else:
        log.log_info(f'Create bot db {mdb_path}')

        conn, cursor = create_matchdb.create_db()
    
    return conn, cursor


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    auth_conn = None
    match_conn = None
    
    def connect_authdb(self):
        if self.auth_conn is None:
            self.auth_conn, self.auth_cursor = conn_authdb()
        return self.auth_conn, self.auth_cursor

    def connect_matchdb(self):
        if self.match_conn is None:
            self.match_conn, self.match_cursor = conn_matchdb()
        return self.match_conn, self.match_cursor

