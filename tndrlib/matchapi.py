# -*- coding: utf-8 -*-

from . import matchdb
from . import utils as ut
from . import messages as mess
from . import authapi

import config

class AbstractApi():
    def __init__(self, user_id, user_name=None):
        self.user_id = str(user_id)
        self.user_name = user_name

        self.userapi = authapi.UserApi(user_id, user_name)
        if not self.userapi.is_full_profile():
            raise Exception("Not full profile")
    
    def lang(self):
        return self.userapi.lang()
    
    def set_lang(self, lang_code):
        self.userapi.set_lang(lang_code)

class MatchApi(AbstractApi):
    def __init__(self, user_id, user_name=None):
        super().__init__(user_id, user_name)
        self.mdb = matchdb.MatchDb(self.user_id)
    
    def get_next_profile(self):
        for profile in self.get_all_profiles():
            yield profile

    def get_prev_profile(self):
        pass

    def like_profile(self, profile_id):
        print("like profile", profile_id)
        self.mdb.set_like(profile_id)

    def dislike_profile(self, profile_id):
        print("dislike profile", profile_id)
        self.mdb.set_dislike(profile_id)

    def complaint_profile(self, profile_id):
        print("report profile", profile_id)

    def get_all_matches(self):
        pass

    def get_all_follower(self):
        pass

    def get_all_profiles(self):
        users_arr = self.userapi.get_confirmed_users()

        return [(authapi.UserApi(id, None).get_short_profile(need_file_name=True), id) for id in users_arr]

    def show_profile(self):
        return self.userapi.get_short_profile(need_file_name=True)