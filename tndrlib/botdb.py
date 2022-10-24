# -*- coding: utf-8 -*-

class BotDb():
    def __init__(self):
        print(f"[INFO BotDb.__init__] connection to db")

    def set_lang(self, lang_code):
        print(f"[INFO BotDb.set_lang] set_lang({lang_code})")

    def get_lang(self):
        return 2