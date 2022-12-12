from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.state import StatesGroup, State

from setting_bot.setting_bot import bot

from tndrlib import matchapi

import config
from config import store_settings
from setting_bot import utils as setting_ut
from match_bot import utils as match_ut
from tndrlib import utils as lib_ut
from tndrlib import messages as mess

from . import places

from match_keyboards import common_boards, swipe_boards
from setting_bot.setting_keyboards import common_boards as setting_common_boards


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

async def next_profile(callback: types.CallbackQuery, state: FSMContext, show_fans=False):
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
            if show_fans:
                profiles = api.get_next_like_for_me()
            else:
                profiles = api.get_next_profile()

        try:
            full_profile = next(profiles)
            next_profile = full_profile[0]
        except StopIteration:
            text = mess.tr(lang, 'no_likes') if show_fans else mess.tr(lang, 'profiles_end')
            await menu(callback.message, state, text, lang)
        except Exception as err:
            raise err
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
            await state.update_data(current_profiles = current_profile, start_msg = message_json, profiles = profiles_json, show_fans = show_fans)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

async def next_match(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()

        await match_ut.check_state(state)

        user_date = await state.get_data()

        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        if "matches" in user_date and user_date["matches"] is not None:
            matches = setting_ut.decode_fsm(user_date["matches"])
            # profiles = user_date["profiles"]
        else:
            matches = api.get_match()

        try:
            if 'flag' in user_date and user_date["flag"]:
                full_profile = matches.prev()
            else:
                if 'hide_flag' in user_date and user_date["hide_flag"]:
                    current_profile = user_date["current_profiles"]
                    api.remove_match(current_profile[2])
                    matches.remove(tuple(current_profile))
                full_profile = matches.next()

            next_profile = full_profile[0]
        except StopIteration:
            text = mess.tr(lang, "end_match")
            await menu(callback.message, state, text, lang)
        except Exception as err:
            if "Iterator is empty" in str(err) or "list index out of range" in str(err):
                text = mess.tr(lang, "end_match")
                await menu(callback.message, state, text, lang)
            else:
                raise err
        else:
            try:
                user = await bot.get_chat_member(chat_id=full_profile[1], user_id=full_profile[1])
                current_username = user.user.username
            except Exception as err:
                if "chat not found" in str(err):
                    await state.update_data(current_profiles = full_profile, flag = False, hide_flag=True)
                    await next_match(callback, state)
                    return
                else:
                    raise err


            text = next_profile["text"]

            if next_profile:
                profile_photo = next_profile["photo_id"]

                photo_path = store_settings['file_store_path'].format(profile_photo)
                photo_path = photo_path.replace("-", "_")

                photo = FSInputFile(photo_path)

                board = swipe_boards.get_match_keyboard(lang, current_username) if matches.max_indx > 1 else swipe_boards.get_alone_match_keyboard(lang, current_username)

                current_msg = await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    parse_mode='markdown',
                    reply_markup=board,
                )
            else:
                text = "пусто"
                await callback.message.answer(text)

            message_json = setting_ut.encode_fsm(current_msg)
            matches_json = setting_ut.encode_fsm(matches)
            await state.update_data(current_profiles = full_profile, start_msg = message_json, matches = matches_json, flag = False, hide_flag = False)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="swipe_callback")
async def swipe_callback(callback: types.CallbackQuery, state: FSMContext):
    await next_profile(callback, state)

@router.callback_query(text="to_menu_callback")
async def to_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await state.get_data()
        await callback.answer()
        await match_ut.check_state(state)
        await state.clear()
        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()
        await menu(callback.message, state, mess.tr(lang, 'menu_msg'), lang)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="show_fans_callback")
async def show_fans_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await match_ut.check_state(state)
        await next_profile(callback, state, True)

        # current_msg = await callback.message.answer(mess.tr(lang, 'no_likes'), reply_markup=swipe_boards.get_to_menu_keyboard(lang))

        # message_json = setting_ut.encode_fsm(current_msg)
        # await state.update_data(start_msg = message_json)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="show_match_callback")
async def show_match_callback(callback: types.CallbackQuery, state: FSMContext):
    # lang = setting_ut.default_lang(callback.message)
    # try:
    #     await callback.answer()
    #     await match_ut.check_state(state)

    #     api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    #     lang = api.lang()

    #     matches = api.get_match()
    #     print(next(matches))
    #     print(next(matches))

    #     current_msg = await callback.message.answer(mess.tr(lang, 'fuck_you'), reply_markup=swipe_boards.get_to_menu_keyboard(lang))

    #     message_json = setting_ut.encode_fsm(current_msg)
    #     await state.update_data(start_msg = message_json)
    # except Exception as err:
    #     await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")
    await next_match(callback, state)

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
    need_remove_like = user_date['show_fans']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.like_profile(current_profile, need_remove_like)

    await next_profile(callback, state, need_remove_like)

@router.callback_query(text="dislike_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("❌")

    user_date = await state.get_data()
    current_profile = user_date['current_profiles']
    need_remove_like = user_date['show_fans']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.dislike_profile(current_profile)

    await next_profile(callback, state, need_remove_like)

@router.callback_query(text="complained_callback")
async def complained_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("🚫")

    user_date = await state.get_data()
    current_profile = user_date['current_profiles']
    need_remove_like = user_date['show_fans']

    api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    api.complaint_profile(current_profile, need_remove_like)

    await next_profile(callback, state, need_remove_like)

@router.callback_query(text="next_callback")
async def like_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("▶️")

    # current_profile = user_date['current_profiles']
    # need_remove_like = user_date['show_fans']

    # api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    # api.like_profile(current_profile, need_remove_like)
    await state.update_data(flag = False)

    await next_match(callback, state)

@router.callback_query(text="hide_callback")
async def like_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    # current_profile = user_date['current_profiles']
    # need_remove_like = user_date['show_fans']

    # api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    # api.like_profile(current_profile, need_remove_like)
    await state.update_data(flag = False, hide_flag=True)

    await next_match(callback, state)

@router.callback_query(text="prev_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("◀️")

    # current_profile = user_date['current_profiles']
    # need_remove_like = user_date['show_fans']

    # api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
    # api.dislike_profile(current_profile)
    await state.update_data(flag = True)

    await next_match(callback, state)

@router.callback_query(text="places_callback")
async def places_callback(callback: types.CallbackQuery, state: FSMContext):
    board = callback.message.reply_markup
    board_json = setting_ut.encode_fsm(board)
    await state.update_data(board = board_json)
    await places.places_callback(callback, state)

@router.callback_query(text="lang_callback")
async def lang_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = setting_ut.default_lang(callback.message)
    try:
        await callback.answer()
        await match_ut.check_state(state)

        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()

        msg = await callback.message.answer(
            mess.tr(lang, 'lang_question'),
            reply_markup=setting_common_boards.LANG_KEYBOARD
        )

        message_json = setting_ut.encode_fsm(msg)
        await state.update_data(start_msg = message_json)

    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")


@router.callback_query(Text(text_startswith="lang_callback_"))
async def delete_account(callback: types.CallbackQuery, state: FSMContext):
    try:
        api = matchapi.MatchApi(callback.from_user.id, callback.from_user.first_name)
        lang = api.lang()
        if 'ru' in callback.data:
            text = mess.tr(lang, 'select_ru_lang')
            api.set_lang(2)
            new_lang = 2
        else:
            text = mess.tr(lang, 'select_en_lang')
            api.set_lang(1)
            new_lang = 1

        await menu(callback.message, state, text, new_lang)

    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, edit_flag=True, utils_flag="m")