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

class MatchApi(AbstractApi):
    def __init__(self, user_id, user_name=None):
        super().__init__(user_id, user_name)
        self.mdb = matchdb.MatchDb(user_id)
    
    def get_next_profile(self):
        for profile in self.get_all_profiles():
            yield profile

    def get_prev_profile(self):
        pass

    def like_profile(self, profile_id):
        pass

    def dislike_profile(self, profile_id):
        pass

    def complaint_profile(self, profile_id):
        pass

    def get_all_matches(self):
        pass

    def get_all_follower(self):
        pass

    def get_all_profiles(self):
        users_arr = self.mdb.get_confirmed_users()
        return [authapi.UserApi(id, None).get_short_profile(need_file_name=True) for id in users_arr]
