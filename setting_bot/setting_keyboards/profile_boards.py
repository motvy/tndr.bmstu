from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tndrlib import messages as mess

PROFILE_EDIT_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'name'), callback_data="name_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'age'), callback_data="age_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'photo'), callback_data="photo_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'gender'), callback_data="gender_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'about'), callback_data="about_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'tags'), callback_data="tags_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'group'), callback_data="study_group_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'vk_link'), callback_data="vk_link_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'view'), callback_data="view_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

PROFILE_EDIT_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'name'), callback_data="name_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'age'), callback_data="age_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'photo'), callback_data="photo_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'gender'), callback_data="gender_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'about'), callback_data="about_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'tags'), callback_data="tags_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'group'), callback_data="study_group_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'vk_link'), callback_data="vk_link_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'view'), callback_data="view_callback")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'to_menu_btn'), callback_data="to_menu_callback"),
        ],
    ]
)

TAGS_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'it'), callback_data="chose_tags_callback_it"),
            InlineKeyboardButton(text=mess.tr(2, 'anime'), callback_data="chose_tags_callback_anime"),
            InlineKeyboardButton(text=mess.tr(2, 'sport'), callback_data="chose_tags_callback_sport")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'study'), callback_data="chose_tags_callback_study"),
            InlineKeyboardButton(text=mess.tr(2, 'music'), callback_data="chose_tags_callback_music"),
            InlineKeyboardButton(text=mess.tr(2, 'party'), callback_data="chose_tags_callback_party")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'books'), callback_data="chose_tags_callback_books"),
            InlineKeyboardButton(text=mess.tr(2, 'games'), callback_data="chose_tags_callback_games"),
            InlineKeyboardButton(text=mess.tr(2, 'science'), callback_data="chose_tags_callback_science")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'films'), callback_data="chose_tags_callback_films"),
            InlineKeyboardButton(text=mess.tr(2, 'food'), callback_data="chose_tags_callback_food"),
            InlineKeyboardButton(text=mess.tr(2, 'languages'), callback_data="chose_tags_callback_languages")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'finance'), callback_data="chose_tags_callback_finance"),
            InlineKeyboardButton(text=mess.tr(2, 'medicine'), callback_data="chose_tags_callback_medicine"),
            InlineKeyboardButton(text=mess.tr(2, 'history'), callback_data="chose_tags_callback_history")
        ],
        [
            InlineKeyboardButton(text=mess.tr(2, 'clear'), callback_data="tags_callback"),
            InlineKeyboardButton(text=mess.tr(2, 'save'), callback_data="end_callback")
        ],
    ]
)

TAGS_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'it'), callback_data="chose_tags_callback_it"),
            InlineKeyboardButton(text=mess.tr(1, 'anime'), callback_data="chose_tags_callback_anime"),
            InlineKeyboardButton(text=mess.tr(1, 'sport'), callback_data="chose_tags_callback_sport")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'study'), callback_data="chose_tags_callback_study"),
            InlineKeyboardButton(text=mess.tr(1, 'music'), callback_data="chose_tags_callback_music"),
            InlineKeyboardButton(text=mess.tr(1, 'party'), callback_data="chose_tags_callback_party")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'books'), callback_data="chose_tags_callback_books"),
            InlineKeyboardButton(text=mess.tr(1, 'games'), callback_data="chose_tags_callback_games"),
            InlineKeyboardButton(text=mess.tr(1, 'science'), callback_data="chose_tags_callback_science")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'films'), callback_data="chose_tags_callback_films"),
            InlineKeyboardButton(text=mess.tr(1, 'food'), callback_data="chose_tags_callback_food"),
            InlineKeyboardButton(text=mess.tr(1, 'languages'), callback_data="chose_tags_callback_languages")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'finance'), callback_data="chose_tags_callback_finance"),
            InlineKeyboardButton(text=mess.tr(1, 'medicine'), callback_data="chose_tags_callback_medicine"),
            InlineKeyboardButton(text=mess.tr(1, 'history'), callback_data="chose_tags_callback_history")
        ],
        [
            InlineKeyboardButton(text=mess.tr(1, 'clear'), callback_data="tags_callback"),
            InlineKeyboardButton(text=mess.tr(1, 'save'), callback_data="end_callback")
        ],
    ]
)

GENDER_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'men_select'), callback_data="chose_callback_m"),
            InlineKeyboardButton(text=mess.tr(2, 'women_select'), callback_data="chose_callback_w"),
        ],
    ]
)

GENDER_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'men_select'), callback_data="chose_callback_m"),
            InlineKeyboardButton(text=mess.tr(1, 'women_select'), callback_data="chose_callback_w"),
        ],
    ]
)

NO_VK_KEYBOARD_RU = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(2, 'no_vk'), callback_data="no_vk_callback"),
        ],
    ],
)

NO_VK_KEYBOARD_EN = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text=mess.tr(1, 'no_vk'), callback_data="no_vk_callback"),
        ],
    ],
)

def get_profile_edit_keyboard(lang):
    return PROFILE_EDIT_KEYBOARD_EN if lang == 1 else PROFILE_EDIT_KEYBOARD_RU

def get_tags_keyboard(lang):
    return TAGS_KEYBOARD_EN if lang == 1 else TAGS_KEYBOARD_RU

def get_gender_keyboard(lang):
    return GENDER_KEYBOARD_EN if lang == 1 else GENDER_KEYBOARD_RU

def get_no_vk_keyboard(lang):
    return NO_VK_KEYBOARD_EN if lang == 1 else NO_VK_KEYBOARD_RU