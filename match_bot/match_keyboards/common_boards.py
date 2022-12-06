from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess
import config


MENU_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'go_swipe_btn'), callback_data="swipe_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'show_fans_btn'), callback_data="show_fans_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'show_match_btn'), callback_data="show_match_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'show_profile_btn'), callback_data="show_profile_callback"),
        ],
    ]
)

MENU_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'go_swipe_btn'), callback_data="swipe_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'show_fans_btn'), callback_data="show_fans_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'show_match_btn'), callback_data="show_match_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'show_profile_btn'), callback_data="show_profile_callback"),
        ],
    ]
)

SETTING_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'setting_btn'), url=config.chat_settings['setting_bot_link'],),
        ],
    ]
)

SETTING_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'setting_btn'), url=config.chat_settings['setting_bot_link'],),
        ],
    ]
)

def get_menu_keyboard(lang):
    return MENU_KEYBOARD_EN if lang == 1 else MENU_KEYBOARD_RU

def get_setting_keyboard(lang):
    return SETTING_KEYBOARD_EN if lang == 1 else SETTING_KEYBOARD_RU