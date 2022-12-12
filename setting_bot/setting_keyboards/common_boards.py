from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess
import config

LANG_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'ru_lang'), callback_data="lang_callback_ru"),
            InlineKeyboardButton(text=mess.tr(1, 'en_lang'), callback_data="lang_callback_en")
        ],
    ]
)

SWIPE_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'swipe_btn'), url=config.chat_settings['swipe_bot_link'],),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

SWIPE_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'swipe_btn'), url=config.chat_settings['swipe_bot_link'],),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

MENU_BOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'my_profile'), callback_data="my_profile_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'delete_profile'), callback_data="delete_profile_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'lang_btn'), callback_data="lang_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'swipe_btn'), callback_data="swipe_callback"),
        ],
    ]
)

MENU_BOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'my_profile'), callback_data="my_profile_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'delete_profile'), callback_data="empty_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'lang_btn'), callback_data="lang_callback"),
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'swipe_btn'), callback_data="empty_callback"),
        ],
    ]
)

TO_MENU_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

TO_MENU_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

def get_to_menu_keyboard(lang):
    return TO_MENU_KEYBOARD_EN if lang == 1 else TO_MENU_KEYBOARD_RU

def get_swipe_keyboard(lang):
    return SWIPE_KEYBOARD_EN if lang == 1 else SWIPE_KEYBOARD_RU

def get_menu_keyboard(lang):
    return MENU_BOARD_EN if lang == 1 else MENU_BOARD_RU