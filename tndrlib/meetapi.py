from . import authdb
from . import utils as ut
from . import authapi
from . import tndriter

from tndrlib import messages as mess
import config

import requests as req
import json

class MeetApi(authapi.UserApi):
    def __init__(self, user_id, second_user_id):
        authapi.UserApi.__init__(self, user_id, None)
        self.second_user_id = str(second_user_id)

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

    def set_matches(self):
        free_time_1 = self.get_free_time(self.user_id)
        free_time_2 = self.get_free_time()
        joint_time = ut.joint_time(free_time_1, free_time_2)

        first_address = self.adb.get_address(self.user_id)
        second_address = self.adb.get_address(self.second_user_id)
        if first_address == second_address:
            info, centre = first_address
            radius = 5000
        else:
            info, centre, radius = second_address[0], 0, 0
        
        tags_1 = self.adb.get_tags(self.user_id)
        tags_2 = self.adb.get_tags(self.second_user_id)
        joint_tags = ' • '.join(ut.joint_tags(tags_1, tags_2))

        self.adb.set_matches(self.second_user_id, centre, radius, joint_tags, joint_time, info)
    
    def get_places(self):
        info = self.adb.get_places_info(self.second_user_id)
        for i in info:
            if i is None or i == "":
                raise Exception("Not full places info")
        
        tags = info['tags'].split(' • ')
        coord = info['centre'].split()

        places_list = []
        for tag in tags:
            req_str = config.default_req.format(tag, coord[1], coord[0], info['radius'])
            res = req.get(req_str).json()
            if res['meta']['code'] == 200:
                for place in res['result']['items']:
                    places_list.append((f"по тегу {tag}:\n\n" + ut.format_place(place), config.two_gis_link.format(place['id'], coord[1], coord[0])))
            else:
                continue
        
        print(*places_list, sep="\n")
        
        return tndriter.MyIter(places_list)

    def get_places_info(self):
        info = self.adb.get_places_info(self.second_user_id)
        if info["centre"] is None or info["centre"] == "":
            result = mess.tr(self.lang, 'places_parametrs') + "\n"
            result += f"{mess.tr(self.lang, 'centre')} {mess.tr(self.lang, 'empty_html')}\n"
            result += f"{mess.tr(self.lang, 'radius', 0)}\n"
        else:
            result = mess.tr(self.lang, 'places_parametrs') + "\n"
            result += f"{mess.tr(self.lang, 'centre')} {info['info']} ({info['centre']})\n"
            result += f"{mess.tr(self.lang, 'radius', info['radius'])}\n"

        tags = [mess.tr(self.lang, tag) for tag in info['tags'].split(' • ')]
        result += f"{mess.tr(self.lang, 'place_tags')} {' • '.join(tags)}"

        return result
    
    def set_centre(self, centre):
        centre = ut.get_centre(centre)
        if centre is None:
            raise Exception('Incorrect centre')
        self.adb.set_centre(self.second_user_id, centre)

    def set_radius(self, radius):
        radius = ut.get_radius(radius)
        if radius is None:
            raise Exception('Incorrect radius')
        self.adb.set_radius(self.second_user_id, radius)

    def set_match_tags(self, tags):
        self.adb.set_match_tags(self.second_user_id, tags)

