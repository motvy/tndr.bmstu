# -*- coding: utf-8 -*-

from . import config
from tndrlib import messages as mess

async def error_handling(msg, err, lang, edit_flag=False):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
    text = str(err) + '\n' + mess.tr(lang, 'contact_support', config.contact_support)
    if edit_flag:
        await msg.edit_text(text=text, parse_mode='markdown', disable_web_page_preview=True, reply_markup=None)
    else:
        await msg.answer(text, parse_mode='markdown', disable_web_page_preview=True)

async def check_state(state):
    user_data = await state.get_data()
    if 'profile_msg' in user_data:
        # keyboard = user_data['reply_markup']
        caption = user_data['caption']
        # print(user_data['profile_msg'])
        await user_data['profile_msg'].edit_caption(caption=caption, reply_markup=None, parse_mode='markdown')
    await state.clear()

def default_lang(msg):
    return 2
