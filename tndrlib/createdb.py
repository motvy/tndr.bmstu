import sqlite3
from bs4 import BeautifulSoup
import requests as req
import re
import os
import json

from config import store_settings as db
from config import schedule_setting as schedule
from tndrlib import utils as ut
from tndrlib import common as log


def create_db():
    conn = sqlite3.connect(db['adb_path'])
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , flags INTEGER NOT NULL DEFAULT 1
                            /*
                                Bits:
                                0 - deleted user
                                1 - wait confirm										
                                2 - active user													
                            */
                            , user_id TEXT NOT NULL								
                            , lang INTEGER NOT NULL DEFAULT 2
                            /*
                                Language:
                                    1 - ru
                                    2 - en
                            */
                            , email TEXT
                            , code TEXT
                            , UNIQUE (user_id)								
                            )''')

    cursor.execute('''CREATE TABLE profiles (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , auth_id INTEGER NOT NULL								
                            , name TEXT
                            , date_of_birth TEXT
                            , photo_id TEXT
                            , gender INTEGER
                            /*
                                Bits:
                                0 - search girl
                                1 - search boy													
                            */
                            , about_user TEXT
                            , tags TEXT
                            , group_id INTEGER
                            , vk_link TEXT
                            , UNIQUE (auth_id)
                            , FOREIGN KEY (auth_id) REFERENCES users(id)
                            , FOREIGN KEY (group_id) REFERENCES groups(id)								
                            )''')

    cursor.execute('''CREATE TABLE groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 
                            , faculty_id INTEGER								
                            , group_name TEXT
                            , schedule TEXT
                            , free_time TEXT
                            , FOREIGN KEY (faculty_id) REFERENCES faculties(id)	
                            , UNIQUE (group_name)								
                            )''')

    cursor.execute('''CREATE TABLE faculties (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 								
                            , faculty_name TEXT
                            , address TEXT
                            , centre TEXT
                            , UNIQUE (faculty_name)				
                            )''')

    cursor.execute('''CREATE TABLE matches (
                            id INTEGER PRIMARY KEY AUTOINCREMENT 								
                            , user_id TEXT NOT NULL	
                            , second_user_id TEXT NOT NULL	
                            , centre TEXT
                            , redius TEXT
                            , tags TEXT
                            , free_time TEXT
                            , info TEXT
                            , FOREIGN KEY (user_id) REFERENCES users (user_id)
                            , FOREIGN KEY (second_user_id) REFERENCES users (user_id)
                            )''')
    
    
    set_schedule(conn, cursor)

    return conn, cursor

def set_schedule(conn, cursor):
    schedule_json = parse_schedule()

    for faculty in schedule_json:
        cursor.execute("insert into faculties (faculty_name) values (?)", (faculty,))
        conn.commit()
        cursor.execute("select id from faculties where faculty_name='{}'".format(faculty,))
        faculty_id = cursor.fetchone()[0]
        print(faculty_id)

        for group in schedule_json[faculty]:
            schedule = schedule_json[faculty][group]
            schedule_txt = json.dumps(schedule)
            free_time = ut.get_free_time(schedule)
            free_time_txt = json.dumps(free_time)

            cursor.execute("insert into groups (faculty_id, group_name, schedule, free_time) values (?, ?, ?, ?)", (faculty_id, group, schedule_txt, free_time_txt))
        
        conn.commit()

    set_address(conn, cursor)

def set_address(conn, cursor):
    cursor.execute("update faculties set address = '{}', centre = '{}' where faculty_name='ИУК' or faculty_name='МК'".format("Баженова 2, Калуга", "54.508676, 36.248576"))
    conn.commit()
    cursor.execute("update faculties set address = '{}', centre = '{}' where faculty_name='К' or faculty_name='ЛТ'".format("1-я Институтская улица, 1, Мытищи", "55.927800, 37.792968"))
    conn.commit()
    cursor.execute("update faculties set address = '{}', centre = '{}' where address is NULL".format("2-я Бауманская улица, Москва", "55.766380, 37.683356"))
    conn.commit()


def parse_schedule():
    groups_path = schedule['groups_path']
    schedule_path = schedule['schedule_path']
    link = schedule['schedule_link']

    if os.path.exists(groups_path):
        log.log_info('Exists schedule')
        with open(groups_path) as f:
            groups_str = f.read()
        
        groups_json = json.loads(groups_str)

    else:
        log.log_info('Start parse schedule')
        resp = req.get(link)
        
        soup = BeautifulSoup(resp.text, 'lxml')

        groups = {}
        for divs in soup.body.find_all('div', class_="panel-body"):
            current_group = ''
            for group_list in divs.find_all('div', class_="btn-group col-xs-10"):
                group_a = group_list.find_all('a')
                for group in group_a:
                    if not current_group:
                        current_group = re.split(r'\d|-' ,group.text.strip())[0]
                        groups[current_group] = {}
                    groups[current_group][group.text.strip()] = group.get('href')
            current_group = ''

        groups_json = groups
        groups_str = json.dumps(groups)
        with open(groups_path, 'w') as f:
            f.write(groups_str)

    if os.path.exists(schedule_path):
        with open(schedule_path) as f:
            schedule_str = f.read()
        schedule_json = json.loads(schedule_str)
    else:
        for faculty in groups_json:
            for group in groups_json[faculty]:
                short_link = groups_json[faculty][group]
                link = 'https://lks.bmstu.ru' + short_link
                resp = req.get(link)
                soup = BeautifulSoup(resp.text, 'lxml')

                sch = {}
                for div in soup.body.find_all('div', class_="col-md-6 hidden-xs"):
                    all_tr = div.table.find_all('tr')
                    day = all_tr[0].text.strip()
                    sch[day] = {}
                    for tr in all_tr[2:]:
                        all_td = tr.find_all('td')
                        time = all_td[0].text.strip()
                        numerator = all_td[1].text.strip()
                        denominator = all_td[2].text.strip() if len(all_td) == 3 else numerator
                        sch[day][time] = {'numerator': numerator, 'denominator': denominator}

                groups_json[faculty][group] = sch

        schedule_json = groups_json
        schedule_str = json.dumps(groups_json)
        with open(schedule_path, 'w') as f:
            f.write(schedule_str)
    
    return schedule_json
