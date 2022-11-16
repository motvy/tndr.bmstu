from . import authdb
from . import utils as ut

import json

class AbstractApi():
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.adb = authdb.AuthDb(user_id)

class ScheduleApi(AbstractApi):
    def __init__(self, user_id):
        AbstractApi.__init__(self, user_id)
    
    def get_free_time(self):
        groups_str = self.adb.get_free_time()
        groups_json = json.loads(groups_str)

        return groups_json



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
