from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests import req_set_user
from keyboards.inline_kbd import get_callback_btns

start = Router()

@start.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    await message.answer(
        "Привет, я твой онлайн помощник. Выбери раздел интересующий тебя:", 
        reply_markup=get_callback_btns(btns={
            'Психологическое благополучие': 'psychology',
        })
            )
    await req_set_user(session, data=message.from_user.id)

@start.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(
        "Выбери раздел интересующий тебя:", 
        reply_markup=get_callback_btns(btns={
            'Психологическое благополучие': 'psychology',
        })
            )