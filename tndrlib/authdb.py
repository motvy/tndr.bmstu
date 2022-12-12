# -*- coding: utf-8 -*-

import config
from tndrlib import utils as ut
from tndrlib import createdb
from tndrlib import common as log
from tndrlib import matchdb
from tndrlib.conn import Database

import os
import sqlite3

class AuthDb():
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.conn , self.cursor = Database().connect_authdb()
        self.mdb = matchdb.MatchDb(self.user_id)


    def confirmed_user(self):
        self.cursor.execute("select * from users where user_id='{}' and flags = 2".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.user_turple_to_dict(info)
    
    def waiting_code_user(self):
        self.cursor.execute("select * from users where user_id='{}' and flags = 1".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.user_turple_to_dict(info)

    def get_user(self):
        self.cursor.execute("select * from users where user_id='{}'".format(self.user_id))
        info = self.cursor.fetchone()
        return ut.user_turple_to_dict(info)

    def get_profile(self):
        self.cursor.execute("select p.* from profiles p, users u where p.auth_id=u.id and u.user_id='{}'".format(self.user_id))
        info = self.cursor.fetchone()

        photo_id = info[4]
        self.cursor.execute("select tg_file_id from files where id='{}'".format(photo_id))
        photo_tg_id = self.cursor.fetchone()
        photo_tg_id = photo_tg_id[0] if photo_tg_id else None

        group_id = info[8]
        self.cursor.execute("select g.group_name from groups g where g.id='{}'".format(group_id))
        group_name = self.cursor.fetchone()
        group_name = group_name[0] if group_name else None

        return ut.profile_turple_to_dict(info, group_name, photo_tg_id)
    
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
            self.conn.commit()

            self.mdb.set_user()
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
        log.log_info(f"reset code from {self.user_id}")


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
        self.cursor.execute("insert into files (tg_file_id) values (?)", (photo_id,))
        
        self.cursor.execute("select id from files where tg_file_id='{}'".format(photo_id))
        id = self.cursor.fetchone()[0]

        self.cursor.execute("update profiles set photo_id='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(id, self.user_id))
        self.conn.commit()

        return id
    
    def set_about(self, about):
        self.cursor.execute("update profiles set about_user='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(about, self.user_id))
        self.conn.commit()
    
    def set_gender(self, gender_flag):
        self.cursor.execute("update profiles set gender='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(gender_flag, self.user_id))
        self.conn.commit()

    def set_vk_link(self, vk_link):
        self.cursor.execute("update profiles set vk_link='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(vk_link, self.user_id))
        self.conn.commit()

        self.mdb.set_vk_link(vk_link)

    def set_study_group(self, study_group):
        group_id = self.get_group_id(study_group)
        self.cursor.execute("update profiles set group_id='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(group_id, self.user_id))
        self.conn.commit()

    def set_tags(self, tags):
        self.cursor.execute("update profiles set tags='{}' from users where users.user_id={} and profiles.auth_id=users.id".format(tags, self.user_id))
        self.conn.commit()

    def get_tags(self, user_id):
        self.cursor.execute("select p.tags from profiles p, users u where p.auth_id=u.id and u.user_id='{}'".format(user_id))
        info = self.cursor.fetchone()[0]

        return info.split(' • ')

    def get_free_time(self, user_id):
        self.cursor.execute("select g.free_time from groups g, profiles p, users u where u.user_id={} and u.id=p.auth_id and p.group_id=g.id".format(user_id))
        info = self.cursor.fetchone()[0]
        return info
    
    def get_schedule(self, user_id):
        self.cursor.execute("select g.schedule from groups g, profiles p, users u where u.user_id={} and u.id=p.auth_id and p.group_id=g.id".format(user_id))
        info = self.cursor.fetchone()[0]
        return info

    def get_confirmed_users(self):
        self.cursor.execute("select user_id from users where flags = 2 and user_id <> '{}'".format(self.user_id))
        users = self.cursor.fetchall()

        return [user[0] for user in users]
    
    def get_address(self, user_id):
        self.cursor.execute("select f.address, f.centre from faculties f, groups g, profiles p, users u where u.user_id = '{}' and u.id = p.auth_id and p.group_id = g.id and g.faculty_id = f.id".format(user_id))
        return self.cursor.fetchone()


    def set_matches(self, second_user_id, centre, radius, tags, free_time, address_info):
        self.cursor.execute("select id from matches where user_id = '{}' and second_user_id = '{}'".format(self.user_id, second_user_id))
        info = self.cursor.fetchone()

        if info is None:
            self.cursor.execute("insert into matches (user_id, second_user_id, centre, radius, tags, free_time, info) values (?, ?, ?, ?, ?, ?, ?)", (self.user_id, second_user_id, centre, radius, tags, free_time, address_info))
        else:
            id = info[0]
            self.cursor.execute("update matches set centre = '{}', radius = '{}', tags = '{}', free_time = '{}', info = '{}' where id = '{}'".format(centre, radius, tags, free_time, address_info, id))
        self.conn.commit()

    def get_joint_time(self, second_user_id):
        self.cursor.execute("select free_time from matches where user_id = '{}' and second_user_id = '{}'".format(self.user_id, second_user_id))
        info = self.cursor.fetchone()[0]
        return info

    def get_joint_tags(self, second_user_id):
        self.cursor.execute("select tags from matches where user_id = '{}' and second_user_id = '{}'".format(self.user_id, second_user_id))
        info = self.cursor.fetchone()[0]
        return info.split(' • ')

    def get_places_info(self, second_user_id):
        self.cursor.execute("select centre, radius, tags, info from matches where user_id = '{}' and second_user_id = '{}'".format(self.user_id, second_user_id))
        info = self.cursor.fetchone()
        return ut.places_info_to_dict(info)

    def set_centre(self, second_user_id, centre):
        self.cursor.execute("update matches set centre = '{}', info='' where user_id = '{}' and second_user_id = '{}'".format(centre, self.user_id, second_user_id))
        self.conn.commit()

    def set_radius(self, second_user_id, radius):
        self.cursor.execute("update matches set radius = '{}' where user_id = '{}' and second_user_id = '{}'".format(radius, self.user_id, second_user_id))
        self.conn.commit()

    def set_match_tags(self, second_user_id, tags):
        self.cursor.execute("update matches set tags = '{}' where user_id = '{}' and second_user_id = '{}'".format(tags, self.user_id, second_user_id))
        self.conn.commit()