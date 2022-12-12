from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram import types

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tndrlib import authapi as botapi
from tndrlib import utils as lib_ut
from setting_bot import utils as bot_ut
from tndrlib import messages as mess

from . import profile

router = Router()

class Login(StatesGroup):
    waiting_email = State()
    waiting_code_query = State()

@router.message(commands=["login", "start"])
async def cmd_login(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        if api.has_confirm():
            return

        lang = api.lang()

        await state.update_data(lang=lang)

        text = mess.tr(lang, 'waiting_email') + '\n' + mess.tr(lang, 'cancel_command')
        msg = await message.answer(text)
        msg_json = bot_ut.encode_fsm(msg)
        current_msg = {'msg': msg_json, 'new_text': mess.tr(lang, 'canceled_login')}
        await state.update_data(current_msg=current_msg)
        await state.set_state(Login.waiting_email)
    except Exception as err:
        print(err)
        await state.clear()
        await lib_ut.error_handling(message, err, lang)


@router.message(commands=["code"])
async def cmd_code(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        # msg = None
        await bot_ut.check_state(state)
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        if api.has_confirm():
            return
        
        if not api.is_he_waiting_code():
            return

        lang = api.lang()

        email = api.has_email()
        if not email:
            raise Exception(mess.tr(lang, 'question_code_invalid'))

        text = mess.tr(lang, 'waiting_code_query', email)
        msg = await message.answer(text)
        msg_json = bot_ut.encode_fsm(msg)

        api.verify()

        current_msg = {'msg': msg_json, 'new_text': mess.tr(lang, 'canceled_login')}
        await state.update_data(current_msg=current_msg)
        await state.set_state(Login.waiting_code_query)

    except Exception as err:
        await state.clear()
        if msg is None:
            await lib_ut.error_handling(message, err, lang)
        else:
            await lib_ut.error_handling(msg, err, lang, edit_flag=True)


@router.message(Login.waiting_email)
async def login(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()
        user_data = await state.get_data()
        current_msg = user_data['current_msg']

        email = message.text.lower().strip()
        await bot_ut.decode_fsm(current_msg['msg']).edit_text(text=mess.tr(lang, 'waiting_email'))
        api.login(email)

        email = api.verify()
        text = mess.tr(lang, 'waiting_code_query', email)
        msg = await message.answer(text)
        msg_json = bot_ut.encode_fsm(msg)
        current_msg['msg'] = msg_json

        await state.update_data(current_msg=current_msg)

        await state.set_state(Login.waiting_code_query)
    except Exception as err:
        if 'Invalid email' in str(err):
            text = mess.tr(lang, 'invalid_email') + '\n' + mess.tr(lang, 'cancel_command')
            msg = await message.answer(text)
            msg_json = bot_ut.encode_fsm(msg)
            current_msg = {'msg': msg_json, 'new_text': mess.tr(lang, 'canceled_login')}
            await state.update_data(current_msg=current_msg)
            await state.set_state(Login.waiting_email)
        else:
            await state.clear()
            await lib_ut.error_handling(message, err, lang)
            raise err

@router.message(Login.waiting_code_query)
async def code_query(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        api = botapi.AuthApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        code = message.text.lower().strip()
        api.confirm(code)

        await message.answer(mess.tr(lang, 'valid_code'))
        await state.clear()
    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(message, err, lang)
    
@router.callback_query(text="delete_profile_callback")
async def delete_account(callback: types.CallbackQuery, state: FSMContext):
    lang = bot_ut.default_lang(callback.message)
    try:
        await bot_ut.check_state(state)
        api = botapi.AuthApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        if not api.has_confirm():
            await callback.message.answer(mess.tr(lang, 'user_for_delete_not_found'))
            return

        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text=mess.tr(lang, 'delete_btn'),
                callback_data="delete_callback_yes"
            )
        )
        builder.add(
            types.InlineKeyboardButton(
                text=mess.tr(lang, 'cancel_btn'),
                callback_data="delete_callback_no"
            )
        )
        msg = await callback.message.answer(
            mess.tr(lang, 'question_delete_account'),
            reply_markup=builder.as_markup(),

        )

        message_json = bot_ut.encode_fsm(msg)
        await state.update_data(current_msg = {'msg': message_json})

    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(callback.message, err, lang)
        raise err

@router.callback_query(Text(text_startswith="delete_callback_"))
async def delete_account(callback: types.CallbackQuery, state: FSMContext):
    try:
        api = botapi.AuthApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()
        if 'yes' in callback.data:
            api.reset_confirm()
            text = mess.tr(lang, 'delete_success')
            await callback.message.edit_text(text=text, reply_markup=None)
        else:
            text = mess.tr(lang, 'delete_canceled')
            await profile.menu(callback.message, state, text, lang)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, edit_flag=True)
