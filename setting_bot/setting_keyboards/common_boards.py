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
    ]
)

SWIPE_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'swipe_btn'), url=config.chat_settings['swipe_bot_link'],),
        ],
    ]
)

def get_swipe_keyboard(lang):
    return SWIPE_KEYBOARD_EN if lang == 1 else SWIPE_KEYBOARD_RU