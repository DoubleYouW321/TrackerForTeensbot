from datetime import date
from aiogram import F, Bot, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import random

from keyboards.inline_kbd import get_callback_btns
import keyboards.inline_kbd as kb
from database.requests import (
    req_add_homework, 
    req_get_my_homeworks, 
    req_delete_homework, 
    req_update_homework_progress, 
    req_get_homework_progress,
    delete_expired_homeworks
)

learning_router = Router()

LEARNING_ADVICES = {
    1: '''📚 Активное чтение. Не просто подчёркивай текст, а делай пометки на полях, формулируй главную мысль каждого абзаца своими словами, пробуй пересказать его по частям, сверяясь с текстом. 🖍️''',
    2: '''📝 Конспектируй с умом. Не списывай абсолютно все. Главную мысль (1–2 строки), 3–4 ключевых пункта, которые её раскрывают, термины и примеры, без которых смысл теряется, делай схемы и таблицы. Помни, конспект — это шпаргалка для твоего мозга, а не копия учебника! 💡''',
    3: '''👨‍🏫 Объясняй материал другим. Попробуй объяснить тему так, как будто ты учишь ребёнка или того, кто совсем не в теме. Это выявит пробелы в понимании. 🎯''',
    4: '''💪 Практикуй, а не просто перечитывай. Решай задачи, проходи тесты прошлых лет, отвечай на вопросы. Активное припоминание — самый эффективный способ перенести знания в долгосрочную память. 🧠''',
    5: '''🎴 Делай карточки по запоминанию дат и понятий. На лицевой стороне — термин или дата. На обороте — точный ответ («Куликовская битва») + ключевой контекст. Откладывай те, в которых ошибся для повторного повторения. Это заставит твой мозг активно работать, экономит время и помогает помнить информацию надолго, а не до завтра. ⏳''',
    6: '''⏱️ Используй технику 25/5: 25 минут полного сосредоточения на материале → 5 минут отдыха. После 4 повторов — длинный перерыв 15–30 минут. Это убережёт от выгорания и повысит концентрацию. ⚡''',
    7: '''🎭 Вложи в стих смысл при выступлении. Представь картинку из стиха, говори так, как будто рассказываешь её другому, смотри на людей и делай паузы на главном, суть: ты — рассказчик, а не говорящий автомат. 🎤''',
    8: '''🧩 Не зубри стих, а собирай пазл. Прочти стих 2-3 раза, вникая в смысл и яркие образы. Дели на куски: разбей на небольшие законченные отрывки (по 2-4 строки). Повторяй вслух по кускам, наращивая, как снежный ком. Подключи тело и эмоции. Ходи по комнате, жестикулируй, читай с выражением. Мышечная и эмоциональная память помогут. 💃''',
    9: '''🌙 Повтори перед сном и утром. Мозг лучше всего консолидирует память во сне. ☀️''',
    10: '''📄 Пиши шпаргалки, даже если не будешь ими пользоваться. Процесс их написания (коротко, тезисно) — и есть лучшее повторение. ✏️''',
    11: '''🌅 Учи сложное утром, повторяй лёгкое вечером. После сна мозг свеж для анализа. Вечером закрепи пройденное — так не будет паники перед сном. 🌃'''
}

class AddHomework(StatesGroup):
    lesson = State()
    description = State()
    deadline = State()

    texts = {
        'AddHomework:lesson': 'Введите название урока, по которому вы хотите добавить ДЗ 📚',
        'AddHomework:description': 'Введите описание задания ✍️',
    }

@learning_router.message(Command('learning'))
async def cmd_learning_message(message: Message, session: AsyncSession, bot: Bot):
    expired = await delete_expired_homeworks(session, message.from_user.id)
    
    for homework in expired:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"❌ <b>Просрочено и удалено!</b>\n\n"
                 f"📚 Предмет: {homework.lesson}\n"
                 f"📝 Задание: {homework.description}\n"
                 f"📅 Дедлайн был: {homework.deadline.strftime('%d.%m.%Y')}",
            parse_mode='HTML'
        )
    
    await message.answer(
        '''🎓 В учебном разделе ты можешь добавлять и сдавать свои домашние задания и отслеживать свой прогресс. А также я могу поделиться с тобой советами по учебе. 💪''', 
        reply_markup=kb.learning_kb
    )

@learning_router.callback_query(or_f(F.data == 'learning', F.data == 'back_to_learning'))
async def cmd_learning_callback(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    await callback.answer('📚')
    
    expired = await delete_expired_homeworks(session, callback.from_user.id)
    
    for homework in expired:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"❌ <b>Просрочено и удалено!</b>\n\n"
                 f"📚 Предмет: {homework.lesson}\n"
                 f"📝 Задание: {homework.description}\n"
                 f"📅 Дедлайн был: {homework.deadline.strftime('%d.%m.%Y')}",
            parse_mode='HTML'
        )
    
    await callback.message.answer(
        '''🎓 В учебном разделе ты можешь добавлять и сдавать свои домашние задания и отслеживать свой прогресс. А также я могу поделиться с тобой советами по учебе. 💪''', 
        reply_markup=kb.learning_kb
    )
# FSM

@learning_router.callback_query(StateFilter('*'), F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.answer('Действия отменены')
    await callback.message.answer('Действия отменены ❌', reply_markup=kb.learning_kb)

@learning_router.callback_query(StateFilter('*'), F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    callback.answer('')
    if current_state == AddHomework.lesson:
        await callback.message.answer('Предыдущего шага нет ⏮️')
        return
    
    previous = None
    for step in AddHomework.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await callback.message.answer(f'Вы вернулись к прошлому шагу ↩️\n{AddHomework.texts[previous.state]}')
            return
        previous = step

@learning_router.callback_query(StateFilter(None), F.data == 'addhomework')
async def cmd_learning(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Введите название предмета: 📖', reply_markup=kb.hw_back_cancel_kb)
    await state.set_state(AddHomework.lesson)

@learning_router.message(AddHomework.lesson)
async def lesson(message: Message, state: FSMContext):
    await state.update_data(lesson=message.text)
    await message.answer('Введите описание домашнего задания: 📝', reply_markup=kb.hw_back_cancel_kb)
    await state.set_state(AddHomework.description)

@learning_router.message(AddHomework.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите дедлайн в формате ДД.ММ.ГГГГ (например: 25.12.2026) 📅', reply_markup=kb.hw_back_cancel_kb)
    await state.set_state(AddHomework.deadline)

@learning_router.message(AddHomework.deadline)
async def deadline(message: Message, state: FSMContext, session: AsyncSession):
    try:
        day, month, year = map(int, message.text.split('.'))
        deadline_date = date(year, month, day)
        
        today = date.today()
        if deadline_date < today:
            await message.answer('❌ Дата дедлайна не может быть в прошлом! Введите корректную дату:')
            return
        
        await state.update_data(deadline=deadline_date, tg_id=message.from_user.id)
        data = await state.get_data()
        await req_add_homework(session, data)
        await message.answer(f'✅ ДЗ добавлено!\n📅 Дедлайн: {deadline_date.strftime("%d.%m.%Y")}', 
                           reply_markup=get_callback_btns(btns={
                               '⬅️ Назад': 'back_to_learning',
                           }))
        await state.clear()
    except (ValueError, AttributeError):
        await message.answer('❌ Неверный формат даты! Используйте ДД.ММ.ГГГГ (например: 25.12.2024):')

# FSM close

@learning_router.callback_query(F.data == 'my_homeworks')
async def cmd_my_homeworks(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    # Проверяем и удаляем просроченные задания
    expired = await delete_expired_homeworks(session, callback.from_user.id)
    
    for homework in expired:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"❌ <b>Просрочено и удалено!</b>\n\n"
                 f"📚 Предмет: {homework.lesson}\n"
                 f"📝 Задание: {homework.description}\n"
                 f"📅 Дедлайн был: {homework.deadline.strftime('%d.%m.%Y')}",
            parse_mode='HTML'
        )
    
    homeworks = await req_get_my_homeworks(session, tg_id=callback.from_user.id)
    
    if not homeworks:
        await callback.message.answer('📭 У вас нет активных домашних заданий', 
                                    reply_markup=get_callback_btns(btns={
                                        '⬅️ Назад': 'back_to_learning',
                                    }))
        return
    
    for homework in homeworks:
        deadline_date = homework.deadline
        days_left = (deadline_date - date.today()).days
        
        deadline_text = f"📅 Дедлайн: {deadline_date.strftime('%d.%m.%Y')}"
        
        if days_left < 0:
            deadline_text += " (просрочено!) ⚠️"
        elif days_left == 0:
            deadline_text += " (сегодня!) ⚠️"
        elif days_left <= 3:
            deadline_text += f" (осталось {days_left} дня!) ⚠️"
        else:
            deadline_text += f" (осталось {days_left} дней)"
        
        await callback.message.answer(
            f'''📚 {homework.lesson}\n📝 {homework.description}\n{deadline_text}''',
            reply_markup=get_callback_btns(btns={
                '✅ Сдать': f'delete_{homework.id}',
            })
        )
    
    await callback.message.answer('📋 Ваши домашние задания', reply_markup=get_callback_btns(btns={
        '⬅️ Назад': 'back_to_learning',
    }))

@learning_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: CallbackQuery, session: AsyncSession):
    homework_id = callback.data.split('_')[-1]
    await req_delete_homework(session, int(homework_id))
    await req_update_homework_progress(session, tg_id=callback.from_user.id)
    await callback.answer('')
    await callback.message.answer('✅ Домашнее задание сдано! 🎉', reply_markup=get_callback_btns(btns={
        '⬅️ Назад': 'back_to_learning',
    }))

@learning_router.callback_query(F.data == 'my_progress')
async def progress(callback: CallbackQuery, session: AsyncSession):
    progress_record = await req_get_homework_progress(session, tg_id=callback.from_user.id)
    
    if progress_record:
        message_text = (
            f"📊 Ваша статистика:\n\n"
            f"✅ Выполнено заданий: {progress_record.completed_count}\n"
            f"❌ Просрочено заданий: {progress_record.expired_count}\n"
            f"🎯 Продолжайте в том же духе! 💪"
        )
        await callback.message.answer(message_text, reply_markup=get_callback_btns(btns={
            '⬅️ Назад': 'back_to_learning',
        }))
    else:
        await callback.message.answer('📭 Вы еще не сдавали домашние задания', reply_markup=get_callback_btns(btns={
            '⬅️ Назад': 'back_to_learning',
        }))
    
    await callback.answer()

@learning_router.callback_query(F.data == 'get_an_advice')
async def get_advice(callback: CallbackQuery):
    await callback.answer('')
    random_adv = random.randint(1, 10)
    advice = LEARNING_ADVICES[random_adv]
    await callback.message.answer(advice, reply_markup=get_callback_btns(btns={
        '⬅️ Назад': 'back_to_learning',
    }))