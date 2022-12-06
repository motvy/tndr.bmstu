from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.state import StatesGroup, State

from tndrlib import matchapi

from config import store_settings
from setting_bot import utils as setting_ut
from match_bot import utils as match_ut
from tndrlib import utils as lib_ut
from tndrlib import messages as mess

from match_keyboards import common_boards, swipe_boards


router = Router()

class Common(StatesGroup):
    waiting_next = State()


@router.message(Command(commands=["start", "menu"]))
async def cmd_menu(message: Message, state: FSMContext):
    lang = setting_ut.default_lang(message)
    try:
        await match_ut.check_state(state)
        api = matchapi.MatchApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        await menu(message, state, mess.tr(lang, 'menu_msg'), lang)
    except Exception as err:
        await lib_ut.error_handling(message, err, lang, utils_flag="m")

async def menu(message: Message, state: FSMContext, text, lang):
    try:
        await match_ut.check_state(state)
        await state.clear()

        start_msg = await message.answer(
                text=text,
                reply_markup=common_boards.get_menu_keyboard(lang)
            )

        message_json = setting_ut.encode_fsm(start_msg)
        await state.update_data(start_msg = message_json, profiles = None)
    except Exception as err:
        await lib_ut.error_handling(message, err, lang, utils_flag="m")

async def next_profile(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()

        await match_ut.check_state(state)

        user_date = await state.get_data()

        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        if "profiles" in user_date and user_date["profiles"] is not None:
            profiles = setting_ut.decode_fsm(user_date["profiles"])
            # profiles = user_date["profiles"]
        else:
            profiles = api.get_next_profile()

        try:
            full_profile = next(profiles)
            next_profile = full_profile[0]
        except Exception as err:
            await menu(callback.message, state, mess.tr(lang, 'profiles_end'), lang)
        else:
            text = next_profile["text"]

            if next_profile:
                profile_photo = next_profile["photo_id"]

                photo_path = store_settings['file_store_path'].format(profile_photo)
                photo_path = photo_path.replace("-", "_")

                photo = FSInputFile(photo_path)

                current_msg = await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    parse_mode='markdown',
                    reply_markup=swipe_boards.get_swipe_keyboard(lang),
                )
            else:
                text = "пусто"
                await callback.message.answer(text)

            message_json = setting_ut.encode_fsm(current_msg)
            current_profile = full_profile[1]
            profiles_json = setting_ut.encode_fsm(profiles)
            await state.update_data(current_profiles = current_profile, start_msg = message_json, profiles = profiles_json)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")


@router.callback_query(text="swipe_callback")
async def swipe_callback(callback: types.CallbackQuery, state: FSMContext):
    await next_profile(callback, state)

@router.callback_query(text="to_menu_callback")
async def to_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    lang = api.lang()
    await menu(callback.message, state, mess.tr(lang, 'menu_msg'), lang)

@router.callback_query(text="show_fans_callback")
async def show_fans_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await match_ut.check_state(state)

        current_msg = await callback.message.answer(mess.tr(lang, 'no_likes'), reply_markup=swipe_boards.get_to_menu_keyboard(lang))

        message_json = setting_ut.encode_fsm(current_msg)
        await state.update_data(start_msg = message_json)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="show_match_callback")
async def show_match_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await match_ut.check_state(state)

        current_msg = await callback.message.answer(mess.tr(lang, 'no_likes'), reply_markup=swipe_boards.get_to_menu_keyboard(lang))

        message_json = setting_ut.encode_fsm(current_msg)
        await state.update_data(start_msg = message_json)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="show_profile_callback")
async def show_profile_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await match_ut.check_state(state)

        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        info = api.show_profile()

        profile_photo = info["photo_id"]
        text = info['text']

        photo_path = store_settings['file_store_path'].format(profile_photo)
        photo_path = photo_path.replace("-", "_")

        photo = FSInputFile(photo_path)

        profile_msg = await callback.message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode='markdown',
            reply_markup=swipe_boards.get_profile_keyboard(lang),
        )

        message_json = setting_ut.encode_fsm(profile_msg)
        await state.update_data(start_msg = message_json)

    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")
    
@router.callback_query(text="like_callback")
async def like_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("❤️")

    user_date = await state.get_data()
    current_profile = user_date['current_profiles']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.like_profile(current_profile)

    await next_profile(callback, state)

@router.callback_query(text="dislike_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("❌")

    user_date = await state.get_data()
    current_profile = user_date['current_profiles']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.dislike_profile(current_profile)

    await next_profile(callback, state)

@router.callback_query(text="complained_callback")
async def complained_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("🚫")

    user_date = await state.get_data()
    current_profile = user_date['current_profiles']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.complaint_profile(current_profile)

    await next_profile(callback, state)