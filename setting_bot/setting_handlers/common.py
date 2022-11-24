from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tndrlib import messages as mess
from tndrlib import authapi as botapi
from tndrlib import meetapi
from tndrlib import utils as lib_ut
from setting_keyboards import common_boards
from setting_bot import utils as bot_ut
import config


router = Router()


# @router.message(Command(commands=["start"]))
# async def cmd_start(message: Message, state: FSMContext):
#     await bot_ut.check_state(state)
#     await state.clear()
#     lang = bot_ut.default_lang(message)
#     await message.answer(text=mess.tr(lang, 'start_msg'))

@router.message(Command(commands=["cancel"]))
# @router.message(Text(text="отмена", text_ignore_case=True))
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

    await state.clear()
    if profile_msg is not None:
        await current_msg.delete()
        await message.delete()
        await state.update_data(profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    else:
        await current_msg.edit_text(text=new_text)
    # await message.answer(text="Действие отменено")

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


# @router.message(Command(commands=["about"]))
# async def cmd_about(message: Message, state: FSMContext):
#     lang = bot_ut.default_lang(message)
#     try:
#         await bot_ut.check_state(state)
#         api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
#         lang = api.lang()

#         await message.answer(text=mess.tr(lang, 'about'))
#     except Exception as err:
#         await lib_ut.error_handling(message, err, lang)


@router.message(commands=["lang"])
async def cmd_delete(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        await message.answer(
            mess.tr(lang, 'lang_question'),
            reply_markup=common_boards.LANG_KEYBOARD
        )

        await state.update_data(api=api, lang=lang)
    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(message, err, lang)
        raise err

@router.callback_query(Text(text_startswith="lang_callback_"))
async def delete_account(callback: types.CallbackQuery):
    try:
        api = botapi.AuthApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()
        if 'ru' in callback.data:
            text = mess.tr(lang, 'select_ru_lang')
            api.set_lang(2)
        else:
            text = mess.tr(lang, 'select_en_lang')
            api.set_lang(1)
        await callback.message.edit_text(text=text, reply_markup=None)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, edit_flag=True)

@router.message(Command(commands=["swipe"]))
async def cmd_swipe(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.UserApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        if api.is_full_profile():
            keyboard = common_boards.get_swipe_keyboard(lang)

            message = await message.answer(text=mess.tr(lang, 'go_swipe'), parse_mode='markdown', disable_web_page_preview=True, reply_markup=keyboard)
        else:
            await message.answer(text=mess.tr(lang, 'not_full_profile'))
    except Exception as err:
        await lib_ut.error_handling(message, err, lang)


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