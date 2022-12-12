# -*- coding: utf-8 -*-

from itertools import tee, islice, chain

from . import tndriter

from . import matchdb
from . import utils as ut
from . import messages as mess
from . import authapi
from . import meetapi

import config

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

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
    
    def get_match(self):
        match_set = self.mdb.get_match()
        match_list = []
        for match_id, user_id in match_set:
            try:
                match_list.append((authapi.UserApi(user_id, None).get_short_profile(need_file_name=True), user_id, match_id))
            except Exception as err:
                if "Has no login" in str(err):
                    continue
                else:
                    raise err

        return tndriter.MyIter(match_list)
    
    def remove_match(self, match_id):
        self.mdb.remove_match(match_id)

    def get_next_like_for_me(self):
        for profile in self.get_all_likes_for_me():
            yield profile

    def get_prev_profile(self):
        pass

    def like_profile(self, profile_id, need_remove_like=False):
        print("like profile", profile_id)
        self.mdb.set_like(profile_id, need_remove_like)
        is_match = self.mdb.set_match(profile_id)

        if is_match:
            meetapi.MeetApi(self.user_id, profile_id).set_matches()

    def dislike_profile(self, profile_id):
        print("dislike profile", profile_id)
        self.mdb.set_dislike(profile_id)

    def complaint_profile(self, profile_id, need_remove_like=False):
        self.mdb.set_report(profile_id, need_remove_like)
        print("report profile", profile_id)

    def get_all_matches(self):
        pass

    def get_all_follower(self):
        pass

    def get_all_profiles(self):
        users_arr = self.userapi.get_confirmed_users()
        profiles_arr = []
        for id in users_arr:
            try:
                profiles_arr.append((authapi.UserApi(id, None).get_short_profile(need_file_name=True), id))
            except Exception as err:
                if "Has no login" in str(err):
                    continue
                else:
                    raise err
        
        return profiles_arr
    
    def get_all_likes_for_me(self):
        users_set = self.mdb.get_likes_for_me(self.user_id)

        likes_arr = []
        for id in users_set:
            try:
                likes_arr.append((authapi.UserApi(id, None).get_short_profile(need_file_name=True), id))
            except Exception as err:
                if "Has no login" in str(err):
                    continue
                else:
                    raise err
        
        return likes_arr

    def show_profile(self):
        return self.userapi.get_short_profile(need_file_name=True)