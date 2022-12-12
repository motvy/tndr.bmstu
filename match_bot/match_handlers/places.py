from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.state import StatesGroup, State

from aiogram import Router
from aiogram.filters.command import Command

from tndrlib import meetapi

from match_keyboards import places_boadrds, swipe_boards
from setting_bot import utils as sut
router = Router()

async def places_callback(callback: types.CallbackQuery, state: FSMContext, split_flag=False):
    await callback.answer()

    text = callback.message.caption
    if split_flag: text = text.rsplit("------------------", 1)[0]
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
    text = api.get_schedule()
    print(text)

    await callback.message.answer(text=text, reply_markup=places_boadrds.get_hide_keyboard(2))

@router.callback_query(text="get_time_callback")
async def back_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    user_date = await state.get_data()
    matches = sut.decode_fsm(user_date["matches"])
    second_user_id = matches.item()[1]

    api = meetapi.MeetApi(callback.from_user.id, second_user_id)
    text = api.get_joint_time()
    print(text)

    await callback.message.answer(text=text, reply_markup=places_boadrds.get_hide_keyboard(2))

@router.callback_query(text="places_menu_callback")
async def hide_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    text = callback.message.caption + "\n------------------\nPlaces"

    await callback.message.edit_caption(caption=text, reply_markup=places_boadrds.get_edit_places_keyboard(2))

@router.callback_query(text="hide_place_callback")
async def hide_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()

@router.callback_query(text="back_to_places_menu_callback")
async def back_to_places_menu_callback(callback: types.CallbackQuery, state: FSMContext):

    await places_callback(callback, state, split_flag=True)
