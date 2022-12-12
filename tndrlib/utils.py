# -*- coding: utf-8 -*-

from setting_bot import utils as sut
from match_bot import utils as mut
from config import schedule_setting as schedule
from tndrlib import common as log
import config

import logging
from logging.handlers import TimedRotatingFileHandler

from datetime import date
import re
import json

async def error_handling(msg, err, lang, edit_flag=False, utils_flag="s"):
    log.log_error(err)
    if utils_flag == "s":
        await sut.error_handling(msg, err, lang, edit_flag)
    else:
        await mut.error_handling(msg, err, lang, edit_flag)

def check_bmstu_email(email):
    match = re.match(r'^\w*@student.bmstu.ru$', email)
    return match.group(0) if match else None

def check_name(name):
    match = re.match(r'^[^\W\d_]*$', name)
    return match.group(0) if match and len(match.group(0)) < 15 else None

def check_about(about):
    return 50 <= len(about) <= 500

def check_vk_link(vk_link):
    match = re.match(r'^https://vk.com/.*$', vk_link)
    vk_link = match.group(0) if match is not None else None
    return vk_link if match and 20 <= len(vk_link) <= 47 else None

def check_study_group(study_group):
    study_group = study_group.lower()
    groups_path = schedule['groups_path']

    with open(groups_path) as f:
        groups_str = f.read()
        
    groups_json = json.loads(groups_str)

    for faculty in groups_json:
        for group in groups_json[faculty]:
            if group.lower() == study_group:
                return True

    return False

def user_turple_to_dict(user_turple):
    if user_turple is None or len(user_turple) == 0:
        user_dict = None
    else:
        user_dict = {
            'flag': user_turple[1],
            'id': user_turple[2],
            'lang': user_turple[3],
            'email': user_turple[4],
            'code': user_turple[5],
        }
    return user_dict

def profile_turple_to_dict(user_turple, group_name, photo_tg_id):
    if user_turple is None or len(user_turple) == 0:
        user_dict = None
    else:
        user_dict = {
            'name': user_turple[2],
            'date_of_birth': user_turple[3],
            'photo_id': photo_tg_id,
            'gender': user_turple[5],
            'about_user': user_turple[6],
            'tags': user_turple[7],
            'study_group': group_name,
            'vk_link': user_turple[9],
        }
    return user_dict, user_turple[4]

def places_info_to_dict(info):
    return {
        'centre': info[0],
        'radius': info[1],
        'tags': info[2],
        'info': info[3],
    }

def is_full_profile(profile):
    if profile is None:
        return False
    else:
        for key in profile:
            if profile[key] is None or profile[key] == '':
                return False

        return True

def get_age(birth_date: str): # format: DD.MM.YYYY
    if not birth_date:
        return None
    try:
        year_now = date.today().year
        date_arr = birth_date.split('.')
        day = int(date_arr[0])
        month = int(date_arr[1])
        year = int(date_arr[2])
        if 1 <= day <= 31 and 1 <= month <= 12 and (year_now - 100) <= year <= (year_now - 14):
            birth_date = date(year, month, day)
            days_in_year = 365.2425
            age = int((date.today() - birth_date).days / days_in_year)
            return age
        else:
            return None
    except Exception:
        return None

def get_free_time(schedule):
    free_time = {}
    for day in schedule:
        free_time[day] = {'numerator': [], 'denominator': []}
        for time in schedule[day]:
            if schedule[day][time]['numerator'] == '':
                free_time[day]['numerator'].append(time)
            if schedule[day][time]['denominator'] == '':
                free_time[day]['denominator'].append(time) 

    return free_time

def joint_time(free_time_1, free_time_2):
    joint_time = {}
    for day in free_time_1:
        joint_time[day] = {
            'numerator': sorted(list(set(free_time_1[day]['numerator']) & set(free_time_2[day]['numerator']))),
            'denominator': sorted(list(set(free_time_1[day]['denominator']) & set(free_time_2[day]['denominator']))),
        }

    joint_time_str = json.dumps(joint_time)

    return joint_time_str

def joint_tags(tags_1, tags_2):
    return set(tags_1) & set(tags_2)

def format_schedule(schedule):
    if schedule == {}:
        raise Exception("No info")

    result = ""
    for day in schedule:
        current = ""
        for time in schedule[day]:
            study_num = schedule[day][time]['numerator']
            study_denom = schedule[day][time]['denominator']
            if study_num == '' and study_denom == '':
                continue
            else:
                current += f"<u>{time}</u>\n"
                if study_num != '': current += f"   ЧС: <i>{study_num}</i>\n"
                if study_denom != '': current += f"   ЗН: <i>{study_denom}</i>\n"
        
        if current != '': result += f"<b>{day}</b>\n{current}\n"
    
    return result

def format_free_time(free_time):
    if free_time == {}:
        raise Exception("No info")

    result = ""
    for day in free_time:
        time_num = free_time[day]['numerator']
        time_denom = free_time[day]['denominator']
        if time_num == [] and time_num == []:
            continue
        else:
            result += f"<b>{day}</b>\n"
            if time_num != []: result += f"<u>ЧС:</u> <i>{' • '.join(time_num)}</i>\n"
            if time_denom != []: result += f"<u>ЗН:</u> <i>{' • '.join(time_denom)}</i>\n"
            result += "\n"

    return result

def format_place(place):
    return place['name'] + "\n" + place["address_name"]


def log_init(logger_name):	
    logger_file_name = config.log_path + f"/{logger_name}.log.txt"
    logger = logging.getLogger(logger_name)

    fileHandler = TimedRotatingFileHandler(logger_file_name, when='midnight', interval=1, backupCount=7, encoding = "UTF-8")

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    # fileHandler = logging.FileHandler(logger_file_name, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler) 

def get_centre(centre):
    return centre

def get_radius(radius):
    try:
        r = int(radius)
    except Exception:
        return None
    else:
        return r if 1000 <= r <= 20000 else None
