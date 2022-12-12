# -*- coding: utf-8 -*-

import config
from tndrlib import messages as mess

from setting_bot import utils as sut

from match_keyboards import common_boards

async def error_handling(msg, err, lang, edit_flag=False):
    if "Not full profile" in str(err) or "Has no login" in str(err):
        text = "Настрой профиль"
        keyboard = common_boards.get_setting_keyboard(lang)

        await msg.answer(text=text, parse_mode='markdown', disable_web_page_preview=True, reply_markup=keyboard)
    else:
        text = str(err) + '\n' + mess.tr(lang, 'contact_support', config.chat_settings['contact_support'])

        if edit_flag:
            await msg.edit_text(text=text, parse_mode='markdown', disable_web_page_preview=True, reply_markup=None)
        else:
            await msg.answer(text, parse_mode='markdown', disable_web_page_preview=True)

def default_lang(msg):
    return 2

async def check_state(state):
    user_date = await state.get_data()
    if "start_msg" in user_date:
        start_msg = sut.decode_fsm(user_date["start_msg"])
        try:
            await start_msg.delete()
        except Exception as err:
            if "message to delete not found" in str(err):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                raise err