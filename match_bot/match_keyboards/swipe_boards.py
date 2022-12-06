from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess
import config

SWIPE_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text="❤️", callback_data="like_callback"),
                        InlineKeyboardButton(text="❌", callback_data="dislike_callback"),
                        InlineKeyboardButton(text="🚫", callback_data="complained_callback")
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'to_menu_btn'), callback_data="to_menu_callback"),
                    ],
                ]
)

SWIPE_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text="❤️", callback_data="like_callback"),
                        InlineKeyboardButton(text="❌", callback_data="dislike_callback"),
                        InlineKeyboardButton(text="🚫", callback_data="complained_callback")
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'to_menu_btn'), callback_data="to_menu_callback"),
                    ],
                ]
)

PROFILE_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'to_menu_btn'), callback_data="to_menu_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'setting_btn'), url=config.chat_settings['setting_bot_link'],),
        ],
    ]
)

PROFILE_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'to_menu_btn'), callback_data="to_menu_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'setting_btn'), url=config.chat_settings['setting_bot_link'],),
        ],
    ]
)

TO_MENU_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Спасибо", callback_data="to_menu_callback"),
        ],
    ]
)

TO_MENU_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Спасибо", callback_data="to_menu_callback"),
        ],
    ]
)

def get_to_menu_keyboard(lang):
    return TO_MENU_KEYBOARD_EN if lang == 1 else TO_MENU_KEYBOARD_RU

def get_swipe_keyboard(lang):
    return SWIPE_KEYBOARD_EN if lang == 1 else SWIPE_KEYBOARD_RU

def get_profile_keyboard(lang):
    return PROFILE_KEYBOARD_EN if lang == 1 else PROFILE_KEYBOARD_RU