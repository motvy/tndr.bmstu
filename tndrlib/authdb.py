# -*- coding: utf-8 -*-

from tndrbot import config
from tndrlib import utils as ut

import os
import sqlite3

class AuthDb():
    def __init__(self, user_id):
        self.user_id = str(user_id)

        db_path = config.adb_path
        if not db_path:
            raise Exception('Path authdb is empty. See config')	

        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        
        self.conn = None
        if os.path.exists(db_path):

            print('Connect cache db', db_path)

            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

        else:
            print('Create bot db', db_path)

            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

            self.cursor.execute('''CREATE TABLE users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT 
                                    , flags INTEGER NOT NULL DEFAULT 1
                                    /*
                                        Bits:
                                        0 - deleted user
                                        1 - wait confirm										
                                        2 - active user													
                                    */
                                    , user_id TEXT NOT NULL								
                                    , lang INTEGER NOT NULL DEFAULT 2
                                    /*
                                        Language:
                                            1 - ru
                                            2 - en
                                    */
                                    , email TEXT
                                    , code TEXT
                                    , UNIQUE (user_id)								
                                    )''')
            
            self.cursor.execute('''CREATE TABLE profiles (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT 
                                    , auth_id INTEGER NOT NULL								
                                    , name TEXT
                                    , date_of_birth TEXT
                                    , photo_id TEXT
                                    , gender INTEGER
                                    /*
                                        Bits:
                                        0 - search girl
                                        1 - search boy													
                                    */
                                    , about_user TEXT
                                    , tags TEXT
                                    , study_group TEXT
                                    , vk_link TEXT
                                    , UNIQUE (auth_id)
                                    , UNIQUE (vk_link)
                                    , FOREIGN KEY (auth_id) REFERENCES users(id)								
                                    )''')


    def confirmed_user(self):
        self.cursor.execute("select * from users where user_id='{}' and flags = 2".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.user_turple_to_dict(info)


    def get_user(self):
        self.cursor.execute("select * from users where user_id='{}'".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.user_turple_to_dict(info)

    def get_profile(self):
        self.cursor.execute("select p.* from profiles p, users u where p.auth_id=u.id and u.user_id='{}'".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.profile_turple_to_dict(info)


    def set_email(self, email):
        if self.get_user() is None:
            self.cursor.execute("insert into users (user_id, email, flags) values (?, ?, ?)", (self.user_id, email, 1))
            self.conn.commit()

            self.cursor.execute("select id from users where user_id='{}'".format(self.user_id))
            id = self.cursor.fetchone()[0]
            print("!!!!!!!!!!!!", id)
            self.cursor.execute("insert into profiles (auth_id) values (?)", (id,))
        else:
            self.cursor.execute("update users set email='{}', flags=1 where user_id={}".format(email, self.user_id))

            self.conn.commit()

    def get_email(self):
        user = self.get_user()
        return user.get('email') if user and user.get('flag') != 0 else None

    def set_code_query(self, code):
        user = self.get_user()
        if user and user.get('flag') != 0:
            self.cursor.execute("update users set code={}, flags=1 where user_id={}".format(code, self.user_id))
            self.conn.commit()
            return user.get('email')
        else:
            return None


    def reset_code_query(self):
        print(f"reset code from {self.user_id}")


    def get_code_query(self):
        user = self.get_user()
        return user.get('code') if user else None


    def confirm(self):
        if self.get_user():
            self.cursor.execute("update users set flags=2 where user_id={}".format(self.user_id))
            self.conn.commit() 
        else:
            return None

    def reset_confirm(self):
        user = self.get_user() 
        if user and user.get('flag') == 2:
            self.cursor.execute("update users set flags=0 where user_id={}".format(self.user_id))
            self.conn.commit() 
            return True
        else:
            return False
    
    def set_lang(self, lang_code):
        print(f'select lang {lang_code}')
        self.cursor.execute("update users set lang={} where user_id={}".format(lang_code, self.user_id))
        self.conn.commit()

    def get_lang(self):
        user = self.get_user()
        return user.get('lang') if user else None
    
    def set_name(self, name):
        self.cursor.execute("update profiles set name='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(name, self.user_id))
        self.conn.commit()
    
    def set_date_of_birth(self, date):
        self.cursor.execute("update profiles set date_of_birth='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(date, self.user_id))
        self.conn.commit() 

    def set_photo(self, photo_id):
        self.cursor.execute("update profiles set photo_id='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(photo_id, self.user_id))
        self.conn.commit()
    
    def set_about(self, about):
        self.cursor.execute("update profiles set about_user='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(about, self.user_id))
        self.conn.commit()
    
    def set_gender(self, gender_flag):
        self.cursor.execute("update profiles set gender='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(gender_flag, self.user_id))
        self.conn.commit()

    def set_vk_link(self, vk_link):
        self.cursor.execute("update profiles set vk_link='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(vk_link, self.user_id))
        self.conn.commit()

    def set_study_group(self, study_group):
        self.cursor.execute("update profiles set study_group='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(study_group, self.user_id))
        self.conn.commit()

    def set_tags(self, tags):
        self.cursor.execute("update profiles set tags='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(tags, self.user_id))
        self.conn.commit()