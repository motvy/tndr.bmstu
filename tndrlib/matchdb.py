# -*- coding: utf-8 -*-

import config
from tndrlib import utils as ut
from tndrlib import createdb
from tndrlib import common as log
from tndrlib import create_matchdb

import os
import sqlite3

class MatchDb():
    def __init__(self, user_id):
        self.user_id = str(user_id)

        db_path = config.store_settings['adb_path']
        if not db_path:
            raise Exception('Path authdb is empty. See config')	

        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        
        self.conn = None
        if os.path.exists(db_path):

            log.log_info(f'Connect cache db {db_path}')

            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

        else:
            log.log_info(f'Create bot db {db_path}')

            self.conn, self.cursor = createdb.create_db()

        self.init_matchdb()
        
    def init_matchdb(self):
        
        db_path = config.store_settings['mdb_path']
        if not db_path:
            raise Exception('Path matchdb is empty. See config')

        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))

        self.match_conn = None
        if os.path.exists(db_path):

            log.log_info(f'Connect cache db {db_path}')

            self.match_conn = sqlite3.connect(db_path)
            self.match_cursor = self.conn.cursor()
        else:
            log.log_info(f'Create bot db {db_path}')

            self.match_conn, self.match_cursor = create_matchdb.create_db()

    def get_confirmed_users(self):
        self.cursor.execute("select user_id from users where flags = 2 and user_id <> '{}'".format(self.user_id))
        users = self.cursor.fetchall()

        return [user[0] for user in users]

    def set_user(self):
        pass