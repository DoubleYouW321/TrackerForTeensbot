from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import os
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests import req_set_comment

feedback_router = Router()

ADMIN = os.getenv("ADMIN")

feedback_markups = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отменить', callback_data='stop')]
])

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()

@feedback_router.callback_query(F.data == 'feedback')
async def callback_feedback_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer("📝 Раздел для отзывов. Напишите свой отзыв:", reply_markup=feedback_markups)
    await state.set_state(FeedbackStates.waiting_for_feedback)

@feedback_router.message(Command("feedback"))
async def cmd_feedback_start(message: Message, state: FSMContext):
    await message.answer("📝 Раздел для отзывов. Напишите свой отзыв:", reply_markup=feedback_markups)
    await state.set_state(FeedbackStates.waiting_for_feedback)

@feedback_router.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user_feedback = message.text
    tg_id = message.from_user.id
    username = message.from_user.username or "Без username"
    first_name = message.from_user.first_name or "Не указано"
    
    admin_message = (
        "📨 Новый отзыв!\n"
        f"👤 Пользователь: {first_name} (@{username})\n"
        f"🆔 ID: {tg_id}\n"
        f"💬 Отзыв: {user_feedback}"
    )

    try:
        await req_set_comment(session, tg_id, user_feedback)
        print(f"✅ Комментарий от {tg_id} сохранен в БД")
        
        await bot.send_message(ADMIN, admin_message)
        await message.answer("✅ Спасибо! Ваш отзыв отправлен администратору.")
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении отзыва: {e}")
        await message.answer("❌ Произошла ошибка при отправке отзыва.")
    
    await state.clear()

@feedback_router.callback_query(F.data == 'stop')
async def process_feedback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()