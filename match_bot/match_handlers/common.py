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

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
            text="Меню",
        )
