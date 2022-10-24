# -*- coding: utf-8 -*-

from tndrbot import utils as ut

from datetime import date

import re

bmstu_faculty = {
    'ак': ('1', '2', '3', '4'),
    'бмт': ('1', '2', '3', '4', '5'),
    'ибм': ('1', '2', '3', '4', '5', '6', '7'),
    'исот': ('', '1', '2'),
    'иу': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'),
    'иук': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    'к': ('1', '2', '3', '4', '5', '6', '7'),
    'л': ('1', '2', '3', '4'),
    'лт': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
    'мк': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    'мт': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'),
    'оэ': ('1', '2'),
    'пс': ('1', '2', '3', '4'),
    'рк': ('1', '2', '3', '4', '5', '6', '7', '8', '9'),
    'ркт': ('1', '2', '3', '4', '5'),
    'рт': ('1', '2', '3', '4', '5'),
    'сгн': ('1', '2', '3', '4'),
    'см': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'),
    'фн': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'), 
    'э': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    'юр': ('', '1', '2', '3'),
}

bmstu_degree = ('', 'а', 'б', 'бв','м')

async def error_handling(msg, err, lang, edit_flag=False):
    print("!!!!!!!!!!", err)
    await ut.error_handling(msg, err, lang, edit_flag)

def check_bmstu_email(email):
    match = re.match(r'^\w*@student.bmstu.ru$', email)
    return match.group(0) if match else None

def check_name(name):
    match = re.match(r'^[^\W\d_]*$', name)
    return match.group(0) if match and len(match.group(0)) < 15 else None

def check_about(about):
    return 100 < len(about) < 500

def check_vk_link(vk_link):
    match = re.match(r'^https://vk.com/.*$', vk_link)
    vk_link = match.group(0) if match is not None else None
    return vk_link if match and 20 <= len(vk_link) <= 47 else None

def check_study_group(study_group):
    study_group = study_group.lower()
    match = re.match(r'^([^\W\d_]+)(\d*)-(\d{2})([^\W\d_]*)$', study_group)
    if not match:
        return False

    faculty = match.group(1)
    faculty_num = match.group(2)
    group = match.group(3)
    degree = match.group(4)
    correct_flag = False
    if faculty in bmstu_faculty and degree in bmstu_degree and faculty_num in bmstu_faculty[faculty]:
        sem = int(group[0])
        group_num = int(group[1])
        month_today = date.today().month
        if 2 <= month_today <= 7:
            if sem > 0 and sem % 2 == 0 and group_num > 0:
                correct_flag = True
        else:
            if sem > 0 and sem % 2 == 1 and group_num > 0:
                correct_flag = True
    
    return correct_flag


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

def profile_turple_to_dict(user_turple):
    if user_turple is None or len(user_turple) == 0:
        user_dict = None
    else:
        user_dict = {
            'name': user_turple[2],
            'date_of_birth': user_turple[3],
            'photo_id': user_turple[4],
            'gender': user_turple[5],
            'about_user': user_turple[6],
            'tags': user_turple[7],
            'study_group': user_turple[8],
            'vk_link': user_turple[9],
        }
    return user_dict

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
