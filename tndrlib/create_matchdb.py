import sqlite3
import re
import os
import json

from config import store_settings as db
from tndrlib import utils as ut
from tndrlib import common as log


def create_db():
    conn = sqlite3.connect(db['mdb_path'])
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE UserActivity (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , user_id TEXT NOT NULL								
                            , like_users_id TEXT
                            , dislike_users_id TEXT
                            , report INTEGER
                            , UNIQUE (user_id)								
                            )''')

    cursor.execute('''CREATE TABLE Matchs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , first_user_id INTEGER NOT NULL
                            , second_user_id INTEGER NOT NULL								
                            , categories TEXT
                            , FOREIGN KEY (first_user_id) REFERENCES UserActivity(id)
                            , FOREIGN KEY (second_user_id) REFERENCES UserActivity(id)								
                            )''')
    
    cursor.execute('''CREATE TABLE VkInfo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , user_id INTEGER NOT NULL
                            , vk_link TEXT								
                            , interests TEXT
                            , FOREIGN KEY (user_id) REFERENCES UserActivity(id)								
                            )''')

    return conn, cursor
