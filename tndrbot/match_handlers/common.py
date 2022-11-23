from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tndrlib import matchapi

from config import store_settings


router = Router()

class Common(StatesGroup):
    waiting_next = State()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text='Посмотреть анкеты',
            callback_data="swipe_callback"
        )
    )
    start_msg = await message.answer("Вы можете посмотреть анкеты!", reply_markup=builder.as_markup())
    await state.update_data(start_msg = start_msg, profiles = None, api = None)
    await state.set_state(Common.waiting_next)


async def next_profile(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    user_date = await state.get_data()

    if "api" in user_date and user_date["api"] is not None:
        api = user_date["api"]
    else:
        api = matchapi.MatchApi(callback.message.from_user.id, callback.message.from_user.first_name)

    if "profiles" in user_date and user_date["profiles"] is not None:
        profiles = user_date["profiles"]
    else:
        profiles = api.get_next_profile()
    
    if "start_msg" in user_date:
        await user_date["start_msg"].delete()

    buttons = [
                [
                    types.InlineKeyboardButton(text="❤️", callback_data="like_callback"),
                    types.InlineKeyboardButton(text="❌", callback_data="dislike_callback"),
                    types.InlineKeyboardButton(text="🚫", callback_data="complained_callback")
                ],
            ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        next_profile = next(profiles)
    except Exception as err:
        await callback.message.answer("Анкеты закончились, попробуйте зайти позже")
    else:
        if next_profile:
            text = next_profile["text"]
            profile_photo = next_profile["photo_id"][:-20]
            photo_path = store_settings['file_store_path'].format(profile_photo)
            photo_path = photo_path.replace("-", "_")

            print(photo_path, "\n\n\n")
            photo = FSInputFile(photo_path)

            current_msg = await callback.message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode='markdown',
                reply_markup=keyboard,
            )
        else:
            text = "пусто"
            await callback.message.answer(text)
        await state.update_data(profiles = profiles, api = api, start_msg = current_msg)

@router.callback_query(text="swipe_callback")
async def swipe_callback(callback: types.CallbackQuery, state: FSMContext):
    await next_profile(callback, state)
    
@router.callback_query(text="like_callback")
async def like_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("❤️")
    await next_profile(callback, state)

@router.callback_query(text="dislike_callback")
async def dislike_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("❌")
    await next_profile(callback, state)

@router.callback_query(text="complained_callback")
async def complained_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("🚫")
    await next_profile(callback, state)