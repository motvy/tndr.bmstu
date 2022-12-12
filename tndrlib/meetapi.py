from . import authdb
from . import utils as ut
from . import authapi

import json

class MeetApi(authapi.UserApi):
    def __init__(self, user_id, second_user_id):
        authapi.UserApi.__init__(self, user_id, None)
        self.second_user_id = str(second_user_id)
        self.user_id = str(user_id)
        self.adb = authdb.AuthDb(user_id)

    def get_free_time(self, user_id=None):
        if user_id is None: user_id = self.second_user_id
        groups_str = self.adb.get_free_time(user_id)
        groups_json = json.loads(groups_str)

        return groups_json
    
    def get_schedule(self, user_id=None):
        if user_id is None: user_id = self.second_user_id
        schedule_str = self.adb.get_schedule(user_id)
        schedule_json = json.loads(schedule_str)

        return ut.format_schedule(schedule_json)
    
    def get_joint_time(self):
        time_str = self.adb.get_joint_time(self.second_user_id)
        time_json = json.loads(time_str)

        return ut.format_free_time(time_json)

    def get_joint_tags(self):
        tags_str = self.adb.get_joint_tags(self.second_user_id)
        tags_json = json.loads(tags_str)

        return tags_json
    
    def get_places_info(self):
        pass

    def set_matches(self):
        free_time_1 = self.get_free_time(self.user_id)
        free_time_2 = self.get_free_time()
        joint_time = ut.joint_time(free_time_1, free_time_2)
        
        tags_1 = self.adb.get_tags(self.user_id)
        tags_2 = self.adb.get_tags(self.second_user_id)
        joint_tags = ' • '.join(ut.joint_tags(tags_1, tags_2))

        self.adb.set_matches(self.second_user_id, 0, 0, joint_tags, joint_time)



"""
Текущие проблемы?
1) Учитыввать сессию
2) Учитывать каникулы
3) Учитывать когда обновляется рассписание
-----------------------------------------
4) Что делать чувакам из разныз корпуов
5) Дать возможность самому задать свободное время?
-----------------------------------------
Если какие-либо проблемы с рассписание, 
"""
