from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types

from tndrlib import messages as mess
from tndrlib import authapi as botapi
from tndrlib import utils as lib_ut
from setting_keyboards import common_boards
from setting_bot import utils as bot_ut
import config

from . import profile

router = Router()

@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data:
        return
    elif 'current_msg' not in user_data:
        return

    current_msg_json = user_data['current_msg']['msg']
    current_msg = bot_ut.decode_fsm(current_msg_json)
    new_text = user_data['current_msg']['new_text']
    if 'profile_msg' in user_data:
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']
    else:
        profile_msg = None

    if profile_msg is not None:
        await current_msg.delete()
        await message.delete()
        await state.update_data(profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    else:
        await current_msg.edit_text(text=new_text)

@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        await message.answer(text=mess.tr(lang, 'help'))
    except Exception as err:
        await lib_ut.error_handling(message, err, lang)


@router.callback_query(text="swipe_callback")
async def swipe_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = bot_ut.default_lang(callback.message)
    try:
        await bot_ut.check_state(state)
        api = botapi.UserApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        if api.is_full_profile():
            keyboard = common_boards.get_swipe_keyboard(lang)
            msg = await callback.message.answer(text=mess.tr(lang, 'go_swipe'), parse_mode='markdown', disable_web_page_preview=True, reply_markup=keyboard)
            message_json = bot_ut.encode_fsm(msg)
            await state.update_data(current_msg= {'msg': message_json})
        else:
            await profile.menu(callback.message, state, mess.tr(lang, 'not_full_profile'))
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang)

async def cmd_lang(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        await message.answer(
            mess.tr(lang, 'lang_question'),
            reply_markup=common_boards.LANG_KEYBOARD
        )

        # await state.update_data(api=api, lang=lang)
    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(message, err, lang)
        raise err

@router.callback_query(text="lang_callback")
async def lang_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = bot_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await bot_ut.check_state(state)

        api = botapi.AuthApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        msg = await callback.message.answer(
            mess.tr(lang, 'lang_question'),
            reply_markup=common_boards.LANG_KEYBOARD
        )

        message_json = bot_ut.encode_fsm(msg)
        await state.update_data(current_msg = {'msg': message_json})

    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang)


@router.callback_query(Text(text_startswith="lang_callback_"))
async def delete_account(callback: types.CallbackQuery, state: FSMContext):
    try:
        api = botapi.AuthApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()
        if 'ru' in callback.data:
            text = mess.tr(lang, 'select_ru_lang')
            api.set_lang(2)
            new_lang = 2
        else:
            text = mess.tr(lang, 'select_en_lang')
            api.set_lang(1)
            new_lang = 1

        await profile.menu(callback.message, state, text, new_lang)

    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, edit_flag=True)


@router.message(Command(commands=["admin"]))
async def cmd_admin(message: Message, state: FSMContext):
    if str(message.from_user.id) not in config.admin_settings['admins_id']:
        return

    lang = bot_ut.default_lang(message)
    try:
        lang = 2

        await message.answer('go fuck yourself')
    except Exception as err:
        await lib_ut.error_handling(message, err, lang)