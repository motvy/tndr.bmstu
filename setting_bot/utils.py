# -*- coding: utf-8 -*-

import jsonpickle

import config
from tndrlib import messages as mess

async def error_handling(msg, err, lang, edit_flag=False):
    text = str(err) + '\n' + mess.tr(lang, 'contact_support', config.chat_settings['contact_support'])
    if edit_flag:
        await msg.edit_text(text=text, parse_mode='markdown', disable_web_page_preview=True, reply_markup=None)
    else:
        await msg.answer(text, parse_mode='markdown', disable_web_page_preview=True)

async def check_state(state):
    user_data = await state.get_data()
    if 'profile_msg' in user_data:
        caption = user_data['caption']
        profile_msg = decode_fsm(user_data['profile_msg'])
        await profile_msg.edit_caption(caption=caption, reply_markup=None, parse_mode='markdown')
    if 'current_msg' in user_data:
        current_msg = decode_fsm(user_data['current_msg']['msg'])
        await current_msg.delete()
    await state.clear()

def default_lang(msg):
    return 2

def encode_fsm(*args):
    result = []
    for arg in args:
        result.append(jsonpickle.encode(arg))
    
    if len(result) == 1: result = result[0]
    
    return result

def decode_fsm(*args):
    result = []
    for arg in args:
        result.append(jsonpickle.decode(arg))
    
    if len(result) == 1: result = result[0]
    
    return result