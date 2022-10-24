# from distutils.command.config import config
import os

from aiogram import Router
from aiogram import Bot

from aiogram.filters import Text
from aiogram.types import Message
from aiogram import types
from aiogram.types import FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.methods import edit_message_media

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tndrlib import authapi as botapi
from tndrlib import utils as lib_ut
from tndrbot import utils as bot_ut
from tndrlib import messages as mess

from tndrbot import config

router = Router()
bot = Bot(token=config.TOKEN)

class Profile(StatesGroup):
    waiting_name = State()
    waiting_date_of_birth = State()
    waiting_photo = State()
    waiting_gender_to_find = State()
    waiting_about = State()
    waiting_voice = State()
    waiting_study_group = State()
    waiting_vk_link = State()
    waiting_tags = State()

@router.message(commands=["profile"])
async def cmd_profile(message: Message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        await bot_ut.check_state(state)
        api = botapi.UserApi(message.from_user.id, message.from_user.first_name)
        lang = api.lang()

        profile_info = api.get_full_profile()

        if profile_info:
            text = profile_info['text']
            photo_id = profile_info['photo_id']
            photo = photo_id if photo_id else FSInputFile(config.no_avatar_path)
        else:
            text = mess.tr(lang, 'profile_empty')
            photo = FSInputFile(config.no_avatar_path)

        # builder = InlineKeyboardBuilder()
        buttons = [
            [types.InlineKeyboardButton(text=mess.tr(lang, 'name'), callback_data="name_callback"),
            types.InlineKeyboardButton(text='Возраст', callback_data="age_callback")],
            [types.InlineKeyboardButton(text='Фото', callback_data="photo_callback"),
            types.InlineKeyboardButton(text=mess.tr(lang, 'gender'), callback_data="gender_callback")],
            [types.InlineKeyboardButton(text='О себе', callback_data="about_callback"),
            types.InlineKeyboardButton(text='Интересы', callback_data="tags_callback")],
            [types.InlineKeyboardButton(text='Группа', callback_data="study_group_callback"),
            types.InlineKeyboardButton(text='Ссылка на вк', callback_data="vk_link_callback")],
            [types.InlineKeyboardButton(text='Как мой профиль видят другие', callback_data="view_callback")],
        ]

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        
        message = await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard,
            parse_mode='markdown',
        )

        await state.update_data(api=api, lang=lang, profile_msg=message, reply_markup=keyboard, caption=text)

    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(message, err, lang)

@router.callback_query(text="name_callback")
async def name_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_name') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_name')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_name)

@router.callback_query(text="age_callback")
async def age_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_date_of_birth') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_date')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_date_of_birth)

@router.callback_query(text="photo_callback")
async def photo_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_photo') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_photo')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_photo)

@router.callback_query(text="about_callback")
async def about_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_about') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_about')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_about)

@router.callback_query(text="gender_callback")
async def gender_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Парень',
        callback_data="chose_callback_m" )
    )
    builder.add(types.InlineKeyboardButton(
        text='Девушка',
        callback_data="chose_callback_w")
    )
    message = await callback.message.answer(
        mess.tr(lang, 'ask_gender'),
        reply_markup=builder.as_markup()
    )
    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_about')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)

@router.callback_query(text="tags_callback")
async def tags_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    buttons = [
        [types.InlineKeyboardButton(text=mess.tr(lang, 'it'), callback_data="chose_tags_callback_it"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'anime'), callback_data="chose_tags_callback_anime"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'sport'), callback_data="chose_tags_callback_sport")],
        [types.InlineKeyboardButton(text=mess.tr(lang, 'study'), callback_data="chose_tags_callback_study"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'music'), callback_data="chose_tags_callback_music"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'party'), callback_data="chose_tags_callback_party")],
        [types.InlineKeyboardButton(text=mess.tr(lang, 'books'), callback_data="chose_tags_callback_books"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'games'), callback_data="chose_tags_callback_games"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'science'), callback_data="chose_tags_callback_science")],
        [types.InlineKeyboardButton(text=mess.tr(lang, 'films'), callback_data="chose_tags_callback_films"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'food'), callback_data="chose_tags_callback_food"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'languages'), callback_data="chose_tags_callback_languages")],
        [types.InlineKeyboardButton(text=mess.tr(lang, 'finance'), callback_data="chose_tags_callback_finance"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'medicine'), callback_data="chose_tags_callback_medicine"),
        types.InlineKeyboardButton(text=mess.tr(lang, 'history'), callback_data="chose_tags_callback_history")],
        [types.InlineKeyboardButton(text='Очистить', callback_data="tags_callback"),
        types.InlineKeyboardButton(text='Сохранить', callback_data="end_callback")],
    ]

    tags_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    text = mess.tr(lang, 'ask_tags') + '\n' + mess.tr(lang, 'cancel_command')
    
    message = await callback.message.answer(
        text,
        reply_markup=tags_keyboard,
        parse_mode='markdown',
    )

    tags = []
    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_about')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption, tags=tags)

@router.callback_query(Text(text_startswith="chose_tags_callback_"))
async def chose_tags_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']
        tags = user_data['tags']

        current_reply_markup = current_msg.reply_markup

        new_tag = mess.tr(lang, callback.data.split('chose_tags_callback_')[-1])
        tags.append(new_tag)

        await callback.answer()

        for el_list in current_reply_markup.inline_keyboard:
            for el in el_list:
                if el.callback_data == callback.data:
                    el_list.remove(el)
                    break
        
        text = ' • '.join(tags) + '\n' + mess.tr(lang, 'cancel_command')
        await current_msg.edit_text(text, reply_markup=current_reply_markup)

        await state.update_data(api=api, lang=lang, current_msg=user_data['current_msg'], profile_msg=profile_msg, reply_markup=keyboard, caption=caption, tags=tags)

    except Exception as err:
        raise err

@router.callback_query(text="end_callback")
async def end_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']
        tags = user_data['tags']
        
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

        api.set_tags(' • '.join(tags))

        new_caption = api.get_full_profile()['text']
        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')

        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)

    except Exception as err:
        await state.clear()
        if 'message is not modified' in str(err):
            await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
        else:
            await lib_ut.error_handling(callback.message, err, lang)

@router.callback_query(text="vk_link_callback")
async def vk_link_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_vk_link') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg={'msg': message, 'new_text': mess.tr(lang, 'cancelled_vk_link')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_vk_link)

@router.callback_query(Text(text_startswith="chose_callback_"))
async def chose_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        
        if 'chose_callback_m' in callback.data:
            api.set_gender(1)
        else:
            api.set_gender(2)
        
        try:
            await callback.message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']
        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)

    except Exception as err:
        await state.clear()
        if 'message is not modified' in str(err):
            await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
        else:
            await lib_ut.error_handling(callback.message, err, lang)
        # await lib_ut.error_handling(callback.message, err, lang, edit_flag=True)

@router.callback_query(text="study_group_callback")
async def study_group_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    api = user_data['api']
    lang = user_data['lang']
    profile_msg = user_data['profile_msg']
    keyboard = user_data['reply_markup']
    caption = user_data['caption']

    if 'current_msg' in user_data:
        current_msg = user_data['current_msg']['msg']
        try:
            await current_msg.delete()
        except Exception as err:
            print(err)

    text = mess.tr(lang, 'ask_study_group') + '\n' + mess.tr(lang, 'cancel_command')
    message = await callback.message.answer(text)

    await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_name')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    await state.set_state(Profile.waiting_study_group)

@router.callback_query(text="view_callback")
async def view_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        profile_info = api.get_short_profile()

        if profile_info:
            text = profile_info['text']
            photo_id = profile_info['photo_id']
            photo = photo_id if photo_id else FSInputFile(config.no_avatar_path)
        else:
            text = mess.tr(lang, 'profile_empty')
            photo = FSInputFile(config.no_avatar_path)
        
        await callback.answer()
        message = await callback.message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode='markdown',
        )

        await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_name')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)

    except Exception as err:
        await state.clear()
        await lib_ut.error_handling(message, err, lang)
        await state.update_data(api=api, lang=lang, profile_msg=message, reply_markup=keyboard, caption=text)

@router.message(Profile.waiting_name)
async def set_name(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        name = message.text.strip()
        # text = mess.tr(lang, 'incorrect_name') if 'after_error' in user_data else mess.tr(lang, 'ask_name')
        # await current_msg.edit_text(text=text)
        api.set_name(name)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
    except Exception as err:
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
        if 'Incorrect name' == str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)

            text = mess.tr(lang, 'incorrect_name') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_name')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_name)            
        elif 'message is not modified' not in str(err):
            await lib_ut.error_handling(message, err, lang)

@router.message(Profile.waiting_date_of_birth)
async def set_date_of_birth(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        date = message.text.strip()
        # text = mess.tr(lang, 'incorrect_date') if 'after_error' in user_data else mess.tr(lang, 'ask_date_of_birth')
        # await current_msg.edit_text(text=text)
        api.set_date_of_birth(date)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
    except Exception as err:
        if 'Incorrect date' in str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)
            text = mess.tr(lang, 'incorrect_date') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_date')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_date_of_birth)
        else:
            await state.clear()
            await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            if 'message is not modified' not in str(err):
                await lib_ut.error_handling(message, err, lang)

@router.message(Profile.waiting_photo)
async def set_photo(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        photo = message.photo
        if photo is None or len(photo) == 0:
            # await current_msg.edit_text(text=mess.tr(lang, 'ask_photo'))
            raise Exception('No photo')

        await current_msg.edit_text(text=mess.tr(lang, 'ask_photo'))
        photo_id = photo[2].file_id
        api.set_photo(photo_id)
        media_photo = InputMediaPhoto(type='photo', media=photo_id, caption=caption, parse_mode='markdown')
    
        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)
    
        file = await bot.get_file(photo_id) # Get file path

        await bot.download_file(file.file_path, config.file_store_path.format(photo_id))

        await edit_message_media.EditMessageMedia(media=media_photo, chat_id=message.chat.id, message_id=profile_msg.message_id, reply_markup=keyboard)
        
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
    except Exception as err:
        if 'No photo' in str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)
            text = mess.tr(lang, 'ask_photo') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_photo')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_photo)
        else:         
            await state.clear()
            await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            if 'message is not modified' not in str(err):
                await lib_ut.error_handling(message, err, lang)

@router.message(Profile.waiting_about)
async def set_about(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api'] 
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        about = message.text.strip()
        text = mess.tr(lang, 'incorrect_about') if 'after_error' in user_data else mess.tr(lang, 'ask_about')
        await current_msg.edit_text(text=text)
        api.set_about(about)
    
        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
    except Exception as err:
        if 'Incorrect about' in str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)
            text = mess.tr(lang, 'incorrect_about') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(after_error=True, api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_about')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_about)
        else:
            await state.clear()
            await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            if 'message is not modified' not in str(err):
                await lib_ut.error_handling(message, err, lang)

@router.message(Profile.waiting_vk_link)
async def set_vk_link(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        vk_link = message.text.strip()
        # text = mess.tr(lang, 'incorrect_name') if 'after_error' in user_data else mess.tr(lang, 'ask_name')
        # await current_msg.edit_text(text=text)
        api.set_vk_link(vk_link)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
    except Exception as err:
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
        if 'Incorrect vk link' == str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)

            text = mess.tr(lang, 'incorrect_vk_link') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_vk_link')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_vk_link)            
        elif 'message is not modified' not in str(err):
            await lib_ut.error_handling(message, err, lang)

@router.message(Profile.waiting_study_group)
async def set_study_group(message, state: FSMContext):
    lang = bot_ut.default_lang(message)
    try:
        user_data = await state.get_data()
        api = user_data['api']
        lang = user_data['lang']
        current_msg = user_data['current_msg']['msg']
        profile_msg = user_data['profile_msg']
        keyboard = user_data['reply_markup']
        caption = user_data['caption']

        study_group = message.text.strip()
        # text = mess.tr(lang, 'incorrect_name') if 'after_error' in user_data else mess.tr(lang, 'ask_name')
        # await current_msg.edit_text(text=text)
        api.set_study_group(study_group)

        try:
            await current_msg.delete()
            await message.delete()
        except Exception as err:
            print(err)

        new_caption = api.get_full_profile()['text']

        await profile_msg.edit_caption(caption=new_caption, reply_markup=keyboard, parse_mode='markdown')
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=new_caption)
    except Exception as err:
        await state.clear()
        await state.update_data(api=api, lang=lang, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
        if 'Incorrect study group' == str(err):
            try:
                await current_msg.delete()
                await message.delete()
            except Exception as err:
                print(err)

            text = mess.tr(lang, 'incorrect_study_group') + '\n' + mess.tr(lang, 'cancel_command')
            message = await message.answer(text)
            await state.update_data(api=api, lang=lang, current_msg= {'msg': message, 'new_text': mess.tr(lang, 'cancelled_name')}, profile_msg=profile_msg, reply_markup=keyboard, caption=caption)
            await state.set_state(Profile.waiting_study_group)            
        elif 'message is not modified' not in str(err):
            await lib_ut.error_handling(message, err, lang)

@router.callback_query(Text(text_startswith="empty_callback"))
async def empty_callback(callback: types.CallbackQuery):
    await callback.answer()