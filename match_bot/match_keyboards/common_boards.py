from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess
import config


MENU_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Смотреть анкеты', callback_data="swipe_callback"),
        ],
        [
            InlineKeyboardButton(text='Посмотреть кому ты нравишься', callback_data="show_fans_callback"),
        ],
        [
            InlineKeyboardButton(text='Посмотреть взаимные лайки', callback_data="show_match_callback"),
        ],
        [
            InlineKeyboardButton(text='Как мою анкету видят другие', callback_data="show_profile_callback"),
        ],
    ]
)