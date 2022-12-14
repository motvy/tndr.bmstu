from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types
from aiogram.fsm.state import StatesGroup, State

from aiogram import Router
from aiogram.filters.command import Command

from tndrlib import meetapi

from match_keyboards import places_boadrds
from setting_bot.setting_keyboards import profile_boards
from setting_bot import utils as sut
from tndrlib import utils as lib_ut
from tndrlib import messages as mess

router = Router()

class Places(StatesGroup):
    waiting_centre = State()
    waiting_radius = State()
    waiting_tags = State()

async def places_callback(callback: types.CallbackQuery, state: FSMContext, split_flag=False):
    await callback.answer()

    text = callback.message.caption
    if split_flag: text = text.rsplit("\n\n", 1)[0]
    await callback.message.edit_caption(caption=text, reply_markup=places_boadrds.get_menu_keyboard(2))

@router.callback_query(text="back_callback")
async def back_callback(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    board = sut.decode_fsm(user_data['board'])
    text = callback.message.caption

    await callback.message.edit_caption(caption=text, reply_markup=board)

@router.callback_query(text="schedule_callback")
async def back_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    user_date = await state.get_data()
    matches = sut.decode_fsm(user_date["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    try:
        text = api.get_schedule()
    except Exception as err:
        if "No info" in str(err):
            text = mess.tr(lang, "no_info")
        else:
            raise err

    await callback.message.answer(text=text, reply_markup=places_boadrds.get_hide_keyboard(2), parse_mode='html')

@router.callback_query(text="get_time_callback")
async def back_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    user_date = await state.get_data()
    matches = sut.decode_fsm(user_date["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    try:
        text = api.get_joint_time()
    except Exception as err:
        if "No info" in str(err):
            text = mess.tr(lang, "no_info")
        else:
            raise err

    await callback.message.answer(text=text, reply_markup=places_boadrds.get_hide_keyboard(2), parse_mode='html')

@router.callback_query(text="places_menu_callback")
async def places_menu_callback(callback: types.CallbackQuery, state: FSMContext, flag=False):
    await callback.answer()

    user_date = await state.get_data()
    matches = sut.decode_fsm(user_date["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    if flag:
        if 'current_msg' in user_date:
            current_msg_json = user_date['current_msg']
            current_msg = sut.decode_fsm(current_msg_json)

            try:
                await current_msg.delete()
            except Exception as err:
                print(err)

        profile_msg = sut.decode_fsm(user_date['profile_msg'])
        text = profile_msg.caption
        photo = profile_msg.photo
        photo_id = photo[-1].file_id
        keyboard = places_boadrds.get_edit_places_keyboard(lang)
        profile_msg = await callback.message.answer_photo(caption=text, photo=photo_id, reply_markup=keyboard, parse_mode="html")
    elif 'profile_msg' in user_date:
        profile_msg = sut.decode_fsm(user_date['profile_msg'])
        text = profile_msg.caption
        keyboard = places_boadrds.get_edit_places_keyboard(lang)

        profile_msg = await profile_msg.edit_caption(caption=text, reply_markup=keyboard, parse_mode='html')
    else:
        text = callback.message.caption + "\n\n" + api.get_places_info()
        keyboard = places_boadrds.get_edit_places_keyboard(lang)

        profile_msg = await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode='html')
    
    profile_msg_json, keyboard_json = sut.encode_fsm(profile_msg, keyboard)
    
    await state.update_data(profile_msg=profile_msg_json, reply_markup=keyboard_json, caption=text)

@router.callback_query(text="hide_place_callback")
async def hide_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()

@router.callback_query(text="back_to_places_menu_callback")
async def back_to_places_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(places=None)

    await places_callback(callback, state, split_flag=True)

@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data:
        return
    elif 'current_msg' not in user_data:
        return

    current_msg_json = user_data['current_msg']
    current_msg = sut.decode_fsm(current_msg_json)
    await current_msg.delete()
    await message.delete()


@router.callback_query(text="edit_centre_callback")
async def edit_centre_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()

    matches = sut.decode_fsm(user_data["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    if 'current_msg' in user_data:
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)

        try:
            await current_msg.delete()
        except Exception as err:
            print(err)
    
    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    text = mess.tr(lang, 'ask_locate') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)
    message_json = sut.encode_fsm(message)

    await state.update_data(current_msg = message_json)
    await state.set_state(Places.waiting_centre)

@router.callback_query(text="edit_radius_callback")
async def edit_radius_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()

    matches = sut.decode_fsm(user_data["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    if 'current_msg' in user_data:
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)

        try:
            await current_msg.delete()
        except Exception as err:
            print(err)
    
    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    text = mess.tr(lang, 'ask_radius') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)
    message_json = sut.encode_fsm(message)

    await state.update_data(current_msg = message_json)
    await state.set_state(Places.waiting_radius)

@router.message(Places.waiting_centre)
async def set_date_of_birth(message, state: FSMContext):
    lang = sut.default_lang(message)
    try:
        user_data = await state.get_data()
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)

        matches, profile_msg, keyboard = sut.decode_fsm(user_data["matches"], user_data['profile_msg'], user_data['reply_markup'])
        caption = user_data['caption']

        second_user_id = matches.item()[1]

        api = meetapi.MeetApi(message.from_user.id, second_user_id)
        lang = api.lang()


        if message.location is None:
            raise Exception('No locate')

        long = message.location.longitude
        lat = message.location.latitude

        geo = f"{lat}, {long}"
        api.set_centre(geo)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = caption.rsplit("\n\n", 1)[0] + "\n\n" + api.get_places_info()

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='html')

        await state.update_data(caption=new_caption)
    except Exception as err:
        if 'No locate' in str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)
            text = mess.tr(lang, 'incorrect_locate') + '\n' + mess.tr(lang, 'cancel_command')
            current_message = await message.answer(text)
            message_json = sut.encode_fsm(current_message)
            await state.update_data(current_msg=message_json)
            await state.set_state(Places.waiting_centre)
        else:
            if 'message is not modified' not in str(err):
                await lib_ut.error_handling(message, err, lang)

@router.message(Places.waiting_radius)
async def set_date_of_birth(message, state: FSMContext):
    lang = sut.default_lang(message)
    try:
        user_data = await state.get_data()
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)

        matches, profile_msg, keyboard = sut.decode_fsm(user_data["matches"], user_data['profile_msg'], user_data['reply_markup'])
        caption = user_data['caption']

        second_user_id = matches.item()[1]

        api = meetapi.MeetApi(message.from_user.id, second_user_id)
        lang = api.lang()


        radius = message.text.strip()
        api.set_radius(radius)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = caption.rsplit("\n\n", 1)[0] + "\n\n" + api.get_places_info()

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='html')

        await state.update_data(caption=new_caption)
    except Exception as err:
        if 'Incorrect radius' in str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)
            text = mess.tr(lang, 'ask_radius') + '\n' + mess.tr(lang, 'cancel_command')
            current_message = await message.answer(text)
            message_json = sut.encode_fsm(current_message)
            await state.update_data(current_msg=message_json)
            await state.set_state(Places.waiting_centre)
        else:
            if 'message is not modified' not in str(err):
                await lib_ut.error_handling(message, err, lang)

@router.callback_query(text="tags_callback")
async def tags_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    matches = sut.decode_fsm(user_data["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    lang = api.lang()

    tags_keyboard = profile_boards.get_tags_keyboard(lang)
    text = mess.tr(lang, 'ask_tags') + '\n' + mess.tr(lang, 'cancel_command')
    
    message = await callback.message.answer(
        text,
        reply_markup=tags_keyboard,
        parse_mode='markdown',
    )
    message_json = sut.encode_fsm(message)
    tags = []

    await state.update_data(current_msg=message_json, profile_msg=profile_msg, reply_markup=keyboard, caption=caption, tags=tags)

@router.callback_query(Text(text_startswith="chose_tags_callback_"))
async def chose_tags_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = sut.default_lang(callback)
    try:
        user_data = await state.get_data()
        current_msg_json = user_data['current_msg']
        current_msg = sut.decode_fsm(current_msg_json)
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']
        tags = user_data['tags']

        current_reply_markup = current_msg.reply_markup

        new_tag = callback.data.split('chose_tags_callback_')[-1]
        tags.append(new_tag)

        await callback.answer()

        for el_list in current_reply_markup.inline_keyboard:
            for el in el_list:
                if el.callback_data == callback.data:
                    el_list.remove(el)
                    break

        matches = sut.decode_fsm(user_data["matches"])
        second_user_id = matches.item()[1]

        api = meetapi.MeetApi(callback.from_user.id, second_user_id)
        lang = api.lang()
        
        tr_tags = [mess.tr(lang, t) for t in tags]
        text = ' • '.join(tr_tags) + '\n' + mess.tr(lang, 'cancel_command')
        await current_msg.edit_text(text, reply_markup=current_reply_markup)

        user_data['current_msg'] = sut.encode_fsm(current_msg)
        await state.update_data(current_msg=user_data['current_msg'], profile_msg=profile_msg, reply_markup=keyboard, caption=caption, tags=tags)

    except Exception as err:
        raise err

@router.callback_query(text="end_callback")
async def end_callback(callback: types.CallbackQuery, state: FSMContext):
    lang = sut.default_lang(callback)
    try:
        user_data = await state.get_data()
        current_msg_json = user_data['current_msg']
        profile_msg_json = user_data['profile_msg']
        keyboard_json = user_data['reply_markup']
        caption = user_data['caption']
        tags = user_data['tags']

        current_msg, profile_msg, keyboard = sut.decode_fsm(current_msg_json, profile_msg_json, keyboard_json)
        
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)
        
        matches = sut.decode_fsm(user_data["matches"])
        second_user_id = matches.item()[1]

        api = meetapi.MeetApi(callback.from_user.id, second_user_id)
        lang = api.lang()

        api.set_match_tags(' • '.join(tags))

        new_caption = caption.rsplit("\n\n", 1)[0] + "\n\n" + api.get_places_info()
        profile_msg = await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='html')
        profile_msg_json = sut.encode_fsm(profile_msg)

        await state.update_data(profile_msg=profile_msg_json, reply_markup=keyboard_json, caption=new_caption)

    except Exception as err:
        if 'message is not modified' in str(err):
            await state.update_data(profile_msg=profile_msg_json, reply_markup=keyboard_json, caption=caption)
        else:
            await lib_ut.error_handling(callback.message, err, lang)

async def next_place(callback: types.CallbackQuery, state: FSMContext):
    lang = sut.default_lang(callback.message)
    try:
        await callback.answer()

        user_date = await state.get_data()
        matches = sut.decode_fsm(user_date["matches"])
        second_user_id = matches.item()[1]

        if 'current_msg' in user_date:
            current_msg_json = user_date['current_msg']
            current_msg = sut.decode_fsm(current_msg_json)
            try:
                await current_msg.delete()
            except Exception as err:
                print(err)

        api = meetapi.MeetApi(callback.from_user.id, second_user_id)
        lang = api.lang()

        if "places" in user_date and user_date["places"] is not None:
            places = sut.decode_fsm(user_date["places"])
        else:
            places = api.get_places()

        try:
            if 'flag' in user_date and user_date["flag"]:
                place = places.prev()
            else:
                place = places.next()

        except StopIteration:
            text = mess.tr(lang, "end_match")
            await places_menu_callback(callback, state, True)
        except Exception as err:
            if "Iterator is empty" in str(err) or "list index out of range" in str(err):
                text = mess.tr(lang, "end_match")
                await places_menu_callback(callback, state, True)
            else:
                raise err
        else:

            if place:
                board = places_boadrds.get_swipe_places_keyboard(lang, place[1]) if places.max_indx > 1 else places_boadrds.get_swipe_places_alone_keyboard(lang, place[1])
                text = place[0]

                current_msg = await callback.message.answer(
                    text=text,
                    parse_mode='markdown',
                    reply_markup=board,
                )
            else:
                text = "пусто"
                await callback.message.answer(text)

            message_json = sut.encode_fsm(current_msg)
            matches_json = sut.encode_fsm(matches)
            places_json = sut.encode_fsm(places)
            await state.update_data(current_msg = message_json, matches = matches_json, flag = False, places=places_json)
    except Exception as err:
        await lib_ut.error_handling(callback.message, err, lang, utils_flag="m")

@router.callback_query(text="show_place_callback")
async def show_match_callback(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(current_msg = user_data['profile_msg'])
    await next_place(callback, state)


@router.callback_query(text="next_place_callback")
async def like_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("▶️")
    await state.update_data(flag = False)

    await next_place(callback, state)


@router.callback_query(text="prev_place_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("◀️")
    await state.update_data(flag = True)

    await next_place(callback, state)

@router.callback_query(text="to_edit_place_menu_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(places=None)

    await places_menu_callback(callback, state, True)
