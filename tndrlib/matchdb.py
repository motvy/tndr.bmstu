# -*- coding: utf-8 -*-

import config
from tndrlib import utils as ut
from tndrlib import common as log
from tndrlib import create_matchdb

import os
import sqlite3

class MatchDb():
    def __init__(self, user_id):
        self.user_id = str(user_id)

        mdb_path = config.store_settings['mdb_path']
        if not mdb_path:
            raise Exception('Path matchdb is empty. See config')

        if not os.path.exists(os.path.dirname(mdb_path)):
            os.makedirs(os.path.dirname(mdb_path))
        
        self.conn = None
        if os.path.exists(mdb_path):

            log.log_info(f'Connect cache db {mdb_path}')

            self.conn = sqlite3.connect(mdb_path)
            self.cursor = self.conn.cursor()

        else:
            log.log_info(f'Create bot db {mdb_path}')

            self.conn, self.cursor = create_matchdb.create_db()

    def set_user(self):
        self.cursor.execute("insert into UserActivity (user_id) values (?)", (self.user_id,))
        self.conn.commit()

        self.cursor.execute("select id from UserActivity where user_id='{}'".format(self.user_id))
        id = self.cursor.fetchone()[0]
        self.cursor.execute("insert into VkInfo (user_activity_id) values (?)", (id,))
        self.conn.commit()

    def set_like(self, user_id, need_remove_like=False):
        user_id = str(user_id)
        likes = self.get_likes(self.user_id)

        likes.add(user_id)
        likes_str = ','.join(likes)
        self.cursor.execute("update UserActivity set like_users_id='{}' where user_id={}".format(likes_str, self.user_id))
        self.conn.commit()

        if need_remove_like:
            likes_for_me = self.get_likes_for_me(self.user_id)
            likes_for_me.remove(user_id)
            likes_for_me_str = ','.join(likes_for_me)
            self.cursor.execute("update UserActivity set likes_for_me='{}' where user_id={}".format(likes_for_me_str, self.user_id))
            self.conn.commit()
        elif self.user_id not in likes_for_me:
            likes_for_me = self.get_likes_for_me(user_id)
            likes_for_me.add(self.user_id)
            likes_for_me_str = ','.join(likes_for_me)
            self.cursor.execute("update UserActivity set likes_for_me='{}' where user_id={}".format(likes_for_me_str, user_id))
            self.conn.commit()

        dislikes = self.get_dislikes(self.user_id)
        if user_id in dislikes:
            dislikes.remove(user_id)
            dislikes_str = ','.join(dislikes)
            self.cursor.execute("update UserActivity set dislike_users_id='{}' where user_id={}".format(dislikes_str, self.user_id))
            self.conn.commit()

    def set_dislike(self, user_id):
        user_id = str(user_id)
        self.cursor.execute("select dislike_users_id from UserActivity where user_id='{}'".format(self.user_id))
        dislikes = self.get_dislikes(self.user_id)

        dislikes.add(user_id)
        dislikes_str = ','.join(dislikes)
        self.cursor.execute("update UserActivity set dislike_users_id='{}' where user_id={}".format(dislikes_str, self.user_id))
        self.conn.commit()

        likes_for_me = self.get_likes_for_me(user_id)

        if self.user_id in likes_for_me:
            likes_for_me.remove(self.user_id)
            likes_for_me_str = ','.join(likes_for_me)
            self.cursor.execute("update UserActivity set likes_for_me='{}' where user_id={}".format(likes_for_me_str, user_id))
            self.conn.commit()

        likes = self.get_likes(self.user_id)
        if user_id in likes:
            likes.remove(user_id)
            likes_str = ','.join(likes)
            self.cursor.execute("update UserActivity set dislike_users_id='{}' where user_id={}".format(likes_str, self.user_id))
            self.conn.commit()
    
    def set_report(self, user_id, need_remove_like=False):
        if need_remove_like:
            likes_for_me = self.get_likes_for_me(self.user_id)
            likes_for_me.remove(user_id)
            likes_for_me_str = ','.join(likes_for_me)
            self.cursor.execute("update UserActivity set likes_for_me='{}' where user_id={}".format(likes_for_me_str, self.user_id))
            self.conn.commit()

    def get_likes(self, user_id):
        self.cursor.execute("select like_users_id from UserActivity where user_id='{}'".format(user_id))
        likes = self.cursor.fetchone()[0]
        return set(likes.split(',')) if likes else set()

    def get_dislikes(self, user_id):
        self.cursor.execute("select dislike_users_id from UserActivity where user_id='{}'".format(user_id))
        dislikes = self.cursor.fetchone()[0]
        return set(dislikes.split(',')) if dislikes else set()
    
    def get_likes_for_me(self, user_id):
        self.cursor.execute("select likes_for_me from UserActivity where user_id='{}'".format(user_id))
        likes = self.cursor.fetchone()[0]
        return set(likes.split(',')) if likes else set()

    def set_vk_link(self, vk_link):
        self.cursor.execute("update VkInfo set vk_link='{}' from UserActivity where UserActivity.user_id={} and VkInfo.user_activity_id=UserActivity.id".format(vk_link, self.user_id))
        self.conn.commit()
    
    def set_match(self, user_id):
        likes = self.get_likes(user_id)

        if self.user_id in likes:
            self.cursor.execute("insert into Matchs (first_user_id, second_user_id) values (?, ?)", (self.user_id, user_id))
            self.conn.commit()
        else:
            print("No match")