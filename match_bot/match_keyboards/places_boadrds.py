from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess
import config


MENU_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'schedule'), callback_data="schedule_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'get_time'), callback_data="get_time_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'places'), callback_data="places_menu_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'back_btn'), callback_data="back_callback"),
                    ],
                ]
)

MENU_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'schedule'), callback_data="schedule_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'get_time'), callback_data="get_time_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'places'), callback_data="places_menu_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'back_btn'), callback_data="back_callback"),
                    ],
                ]
)

HIDE_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(1, "hide"), callback_data="hide_place_callback"),
                    ],
                ]
)

HIDE_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(2, "hide"), callback_data="hide_place_callback"),
                    ],
                ]
)

EDIT_PLACES_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'get_place'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'edit_centre'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'edit_radius'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'edit_tags'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(1, 'back_btn'), callback_data="back_to_places_menu_callback"),
                    ], 
                ]
)

EDIT_PLACES_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'get_place'), callback_data="empty_callback"),
                    ],       
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'edit_centre'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'edit_radius'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'edit_tags'), callback_data="empty_callback"),
                    ],
                    [
                        InlineKeyboardButton(text=mess.tr(2, 'back_btn'), callback_data="back_to_places_menu_callback"),
                    ], 
                ]
)

def get_menu_keyboard(lang):
    return MENU_KEYBOARD_EN if lang == 1 else MENU_KEYBOARD_RU

def get_hide_keyboard(lang):
    return HIDE_KEYBOARD_EN if lang == 1 else HIDE_KEYBOARD_RU

def get_edit_places_keyboard(lang):
    return EDIT_PLACES_KEYBOARD_EN if lang == 1 else EDIT_PLACES_KEYBOARD_RU