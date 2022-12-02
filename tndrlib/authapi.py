# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import authdb
from . import utils as ut
from . import messages as mess

import config

from threading import Timer
import smtplib
import random

class AbstractApi():
    def __init__(self, user_id, user_name=None):
        self.user_id = str(user_id)
        self.user_name = user_name
        self.adb = authdb.AuthDb(user_id)

    def lang(self):
        lang = self.adb.get_lang()
        return lang
    
    def set_lang(self, lang_code):
        self.adb.set_lang(lang_code)


class AuthApi(AbstractApi):
    def __init__(self, user_id, user_name):
        AbstractApi.__init__(self, user_id, user_name)
        self.adb = authdb.AuthDb(user_id)
        self.current_thread = None
    
    def has_confirm(self):
        return True and self.adb.confirmed_user()
    
    def is_he_waiting_code(self):
        return True and self.adb.waiting_code_user()
    
    def login(self, email):
        email = ut.check_bmstu_email(email)
        if email:
            self.adb.set_email(email)
            # self.verify(email)
        else:
            raise Exception('Invalid email')

    def has_email(self):
        email = self.adb.get_email()
        return email
            # raise Exception(mess.tr(self.lang(), 'question_code_invalid'))        

    def verify(self):
        
        code = random.randint(1000, 9999)

        email = self.adb.set_code_query(str(code))
        if not email:
            raise Exception(mess.tr(self.lang(), 'question_code_invalid'))

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()

        login = config.settings_bot_settings['bot_login']
        password = config.settings_bot_settings['bot_password']

        smtpObj.login(login, password)

        message = MIMEMultipart("alternative")
        message["Subject"] = "Код подтверждения BMSTU.TNDR"
        message["From"] = login
        message["To"] = email
        email_html = mess.tr(self.lang(), 'email_html_text', self.user_name, str(code))
        text = MIMEText(email_html, "html")
        message.attach(text)

        smtpObj.sendmail(login, email, message.as_string())

        return email

        # timer = Timer(20.0, self.reset_timer())
        # self.current_thread = timer
        # timer.start()
        # print("qqqqqqqqqqqqqqqqqqqqqqqq")
        # return True
    
    def reset_timer(self):
        if self.current_thread:
            self.current_thread.cancel()
        self.adb.reset_code_query()

    def confirm(self, code):
        correct_code = self.adb.get_code_query()
        if not correct_code:
            raise Exception("Exception in confirm")
        if correct_code != str(code):
            raise Exception(mess.tr(self.lang(), 'invalid_code'))
        
        self.adb.confirm()
        
        # if self.current_thread:
        #     self.reset_timer()
    
    def reset_confirm(self):
        # raise Exception("Exception in reset confirm")
        if not self.adb.reset_confirm():
            raise Exception("Exception in reset confirm")


class UserApi(AbstractApi):
    def __init__(self, user_id, user_name):
        AbstractApi.__init__(self, user_id, user_name)

        if not authdb.AuthDb(user_id).confirmed_user():
            raise Exception(mess.tr(self.lang(), 'has_no_login'))
       
    def has_profile(self):
        return self.adb.get_profile() and True

    def get_short_profile(self, need_file_name=False):
        profile, file_name = self.adb.get_profile()
        info = None
        if profile:
            name = profile['name']
            age = ut.get_age(profile['date_of_birth'])
            about = profile['about_user']
            photo_id = file_name if need_file_name else profile['photo_id']

            tags = [mess.tr(self.lang(), tag) for tag in profile['tags'].split(' • ')] if profile['tags'] else None

            text = name if name else mess.tr(self.lang(), 'without_name')
            text += f', {age}\n' if age else '\n'
            text += f'\n{about}' if about else ''
            text += '\n\n' + ' • '.join(tags) if tags else ''

            info = {
                'text': text.replace('None', mess.tr(self.lang(), 'none_info')),
                'photo_id': photo_id,
            }

        return info

    def get_full_profile(self):
        profile, file_name = self.adb.get_profile()
        info = None
        text = ''
        if profile:
            name = profile['name'] if profile['name'] else mess.tr(self.lang(), 'none_info')
            date = profile['date_of_birth'] if profile['date_of_birth'] else mess.tr(self.lang(), 'none_info')
            about = profile['about_user'] if profile['about_user'] else mess.tr(self.lang(), 'none_info')
            gender = mess.tr(self.lang(), 'men_select') if profile['gender'] == 1 else mess.tr(self.lang(), 'women_select') if profile['gender'] == 2 else mess.tr(self.lang(), 'none_info')
            photo_id = profile['photo_id']
            tags = [mess.tr(self.lang(), tag) for tag in profile['tags'].split(' • ')] if profile['tags'] else None
            tags = ' • '.join(tags) if tags else mess.tr(self.lang(), 'none_info')
            vk_link = profile['vk_link'] if profile['vk_link'] else mess.tr(self.lang(), 'none_info')
            vk_link = mess.tr(self.lang(), 'no') if vk_link == 'no' else vk_link
            study_group = profile['study_group'] if profile['study_group'] else mess.tr(self.lang(), 'none_info')

            text += mess.tr(self.lang(), 'name_info', name) + '\n'
            text += mess.tr(self.lang(), 'date_info', date) + '\n'
            text += mess.tr(self.lang(), 'about_info', about) + '\n'
            text += mess.tr(self.lang(), 'gender_info', gender) + '\n'
            text += mess.tr(self.lang(), 'study_group_info', study_group) + '\n'
            text += mess.tr(self.lang(), 'vk_link_info', vk_link) + '\n'
            text += mess.tr(self.lang(), 'tags_info', tags) + '\n'

            info = {
                'text': text,
                'photo_id': photo_id,
            }

        return info
    
    def set_name(self, name):
        name = ut.check_name(name)
        if name is None:
            raise Exception('Incorrect name')
        self.adb.set_name(name)
    
    def set_photo(self, photo_id):
        return self.adb.set_photo(photo_id)
    
    def set_date_of_birth(self, date):
        age = ut.get_age(date)
        if age is None:
            raise Exception('Incorrect date')
        self.adb.set_date_of_birth(date)
    
    def set_about(self, about):
        if not ut.check_about(about):
            raise Exception(f'Incorrect about;{len(about)};{about}')
        self.adb.set_about(about)
    
    def set_gender(self, gender_flag):
        self.adb.set_gender(gender_flag)

    def set_vk_link(self, vk_link):
        if vk_link != 'no':
            vk_link = ut.check_vk_link(vk_link)
            if vk_link is None:
                raise Exception('Incorrect vk link')
        self.adb.set_vk_link(vk_link)

    def set_study_group(self, study_group):
        flag = ut.check_study_group(study_group)
        if not flag:
            raise Exception('Incorrect study group')
        self.adb.set_study_group(study_group.upper())

    def set_tags(self, tags):
        self.adb.set_tags(tags)

    def is_full_profile(self):
        profile, file_name = self.adb.get_profile()
        return ut.is_full_profile(profile)
    
