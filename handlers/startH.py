from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests import req_set_user
from keyboards.inline_kbd import get_callback_btns

start = Router()

PHOTO = 'AgACAgIAAxkBAAICOWl80wErPSQTFRvCyR-0gzSBx018AAJGEmsbKX7gS0k2C47biAijAQADAgADeQADOAQ'

@start.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    photo = PHOTO
    await message.answer_photo(photo=photo, caption='''Привет! 👋 Я Помогатор — твой личный помощник.

Со мной ты сможешь:
📚 Легче учиться
🧠 Лучше чувствовать
💪 Следить за здоровьем и активностью

Всё в одном месте, просто и безопасно. Поехали? Выбери раздел ниже ⬇️''', 
        reply_markup=get_callback_btns(btns={
            '🧠 Психологическое благополучие': 'psychology',
            '🎓 Учебный раздел': 'learning',
            '💪 Здоровье и Активность': 'health',
            '🤖 Оценка состояния': 'conditions',
            '🏀 Хобби': 'hobbies',
            '💬 Отправить отзыв': 'feedback',
        }))
    await req_set_user(session, data=message.from_user.id)

@start.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(
        "Выбери раздел интересующий тебя:", 
        reply_markup=get_callback_btns(btns={
            '🧠 Психологическое благополучие': 'psychology',
            '🎓 Учебный раздел': 'learning',
            '💪 Здоровье и Активность': 'health',
            '🤖 Оценка состояния': 'conditions',
            '🏀 Хобби': 'hobbies',
            '💬 Отправить отзыв': 'feedback',
        })
            )
    