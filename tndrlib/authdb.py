# -*- coding: utf-8 -*-

from tndrbot import config
from tndrlib import utils as ut
from tndrlib import createdb


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

            self.conn, self.cursor = createdb.create_db()


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

        group_id = info[8]
        self.cursor.execute("select g.group_name from groups g where g.id='{}'".format(group_id))
        group_name = self.cursor.fetchone()
        group_name = group_name[0] if group_name else None

        return ut.profile_turple_to_dict(info, group_name)
    
    def get_group_id(self, group):
        group = group.upper()
        self.cursor.execute("select g.id from groups g where g.group_name='{}'".format(group))
        return self.cursor.fetchone()[0]

    def set_email(self, email):
        if self.get_user() is None:
            self.cursor.execute("insert into users (user_id, email, flags) values (?, ?, ?)", (self.user_id, email, 1))
            self.conn.commit()

            self.cursor.execute("select id from users where user_id='{}'".format(self.user_id))
            id = self.cursor.fetchone()[0]
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
        group_id = self.get_group_id(study_group)
        self.cursor.execute("update profiles set group_id='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(group_id, self.user_id))
        self.conn.commit()

    def set_tags(self, tags):
        self.cursor.execute("update profiles set tags='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(tags, self.user_id))
        self.conn.commit()

    def get_free_time(self):
        self.cursor.execute("select g.free_time from groups g, profiles p, users u where u.user_id={} and u.id=p.auth_id and p.group_id=g.id".format(self.user_id))
        info = self.cursor.fetchone()[0]
        return info
