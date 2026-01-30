from aiogram import F, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

import keyboards.inline_kbd as kb
from database.requests import req_save_daily_metrics, req_get_today_metrics, req_get_user_category

health_router = Router()

ADVICES = {
    1: 'Вода и мозг 💧\nОбезвоживание всего на 2% уже снижает концентрацию и кратковременную память. Стакан воды утром — лучший "будильник" для мозга!',
    2: 'Сон и иммунитет 😴\nВо время глубокого сна организм вырабатывает цитокины — белки, которые борются с инфекциями. Хронический недосып = открытые ворота для болезней.',
    3: 'Спорт против стресса 🏃‍♂️\n30 минут быстрой ходьбы не только сжигают калории, но и снижают уровень гормона стресса (кортизола) и повышают уровень эндорфинов.',
    4: 'Осанка и настроение 🧍\nСутулость усиливает чувство тревоги и бессилия. Расправь плечи и подними голову на 1 минуту — это сигнализирует мозгу, что ты в безопасности и уверен в себе.',
    5: 'Сила жевания 🍽️\nТщательное пережёвывание пищи (20-30 раз) улучшает пищеварение, помогает контролировать вес и даже снижает стресс, действуя как медитация.',
    6: 'Холодный душ 🚿\nКраткий холодный душ (30-60 сек) с утра повышает бодрость, ускоряет метаболизм и укрепляет устойчивость к стрессу.',
    7: 'Солнечный витамин D ☀️\n15-20 минут на дневном свету (даже в пасмурную погоду) значительно улучшают настроение и регулируют сон благодаря выработке витамина D и серотонина.',
    8: 'Сахарные качели 🍬\nБыстрые углеводы (сладости, выпечка) вызывают резкий скачок, а затем спад энергии и настроения. Белок и клетчатка дают ровную энергию на часы.',
    9: 'Микро-разминка 🏋️‍♂️\n5-минутная разминка каждый час сидячей работы ускоряет обмен веществ на 20% и снижает риски для сердечно-сосудистой системы.',
    10: 'Мозг на прогулке 🌳\nПрогулка на свежем воздухе, особенно в зелёных зонах, увеличивает приток крови к префронтальной коре мозга, отвечающей за креативность и решение задач.',
}

class MetricsStates(StatesGroup):
    waiting_for_water = State()
    waiting_for_sleep = State()
    waiting_for_steps = State()

@health_router.message(Command('health'))
async def cmd_health_message(message: Message):
    await message.answer(
        'В разделе Здоровье и Активность ты можешь получить полезный совет из базы знаний, а также записывать и редактировать свои физические показатели:\n\n• Количество выпитых стаканов воды 💧\n• Часы сна 😴\n• Количество пройденных шагов 👣\n\nСравнивай их с нормой и следи за прогрессом!', 
        reply_markup=kb.health
    )

@health_router.callback_query(or_f(F.data == 'health', F.data == 'back_to_health'))
async def cmd_health_callback(callback: CallbackQuery):
    await callback.answer('💪')
    await callback.message.answer(
        'В разделе Здоровье и Активность ты можешь получить полезный совет из базы знаний, а также записывать и редактировать свои физические показатели:\n\n• Количество выпитых стаканов воды 💧\n• Часы сна 😴\n• Количество пройденных шагов 👣\n\nСравнивай их с нормой и следи за прогрессом!', 
        reply_markup=kb.health
    )

@health_router.callback_query(F.data == 'categories')
async def handle_datas_button(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer('')
    category = await req_get_user_category(session, callback.from_user.id)
    today_metrics = await req_get_today_metrics(session, callback.from_user.id)
    if today_metrics and (today_metrics['water_glasses'] > 0 or today_metrics['sleep_hours'] > 0 or today_metrics['steps'] > 0):
        text = f"📊 У тебя уже есть данные за сегодня:\n\n💧 Вода: {today_metrics['water_glasses']}/{category['water']} стаканов\n😴 Сон: {today_metrics['sleep_hours']}/{category['hours']} часов\n👣 Шаги: {today_metrics['steps']}/{category['steps']}\n\nХочешь обновить данные? ✏️"
        await callback.message.answer(text, reply_markup=kb.update_metrics)
    else:
        text = f"Твои целевые показатели:\n\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}\n\nВведи количество выпитых стаканов воды:"
        await callback.message.answer(text, reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_water)

@health_router.message(MetricsStates.waiting_for_water)
async def process_water_input(message: Message, state: FSMContext, session: AsyncSession):
    try:
        water_glasses = int(message.text)
        if water_glasses < 0:
            raise ValueError
        await state.update_data(water=water_glasses)
        category = await req_get_user_category(session, message.from_user.id)
        await message.answer(f"Цель по сну: {category['hours']} часов 😴\nВведи количество часов сна:", reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_sleep)
    except ValueError:
        await message.answer("Пожалуйста, введи целое число (например: 8) 💧")

@health_router.message(MetricsStates.waiting_for_sleep)
async def process_sleep_input(message: Message, state: FSMContext, session: AsyncSession):
    try:
        sleep_hours = float(message.text)
        if sleep_hours < 0:
            raise ValueError
        await state.update_data(sleep=sleep_hours)
        category = await req_get_user_category(session, message.from_user.id)
        await message.answer(f"Цель по шагам: {category['steps']} 👣\nВведи количество шагов за день:", reply_markup=kb.cancel_keyboard)
        await state.set_state(MetricsStates.waiting_for_steps)
    except ValueError:
        await message.answer("Пожалуйста, введи число (например: 7.5) 😴")

@health_router.message(MetricsStates.waiting_for_steps)
async def process_steps_input(message: Message, state: FSMContext, session: AsyncSession):
    try:
        steps = int(message.text)
        if steps < 0:
            raise ValueError
        data = await state.get_data()
        metrics = await req_save_daily_metrics(session, message.from_user.id, data['water'], data['sleep'], steps)
        category = await req_get_user_category(session, message.from_user.id)
        water_status = "✅" if metrics['water_glasses'] >= category['water'] else "❌"
        sleep_status = "✅" if metrics['sleep_hours'] >= category['hours'] else "❌"
        steps_status = "✅" if metrics['steps'] >= category['steps'] else "❌"
        await message.answer(f"✅ Данные сохранены!\n\n{water_status} Вода: {metrics['water_glasses']}/{category['water']} стаканов\n{sleep_status} Сон: {metrics['sleep_hours']}/{category['hours']} часов\n{steps_status} Шаги: {metrics['steps']}/{category['steps']}\n\nДата: {metrics['date']}", reply_markup=kb.back_to_heath)
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введи целое число (например: 10000) 👣")

@health_router.callback_query(F.data == 'my_metrics')
async def show_my_metrics(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('')
    category = await req_get_user_category(session, callback.from_user.id)
    metrics = await req_get_today_metrics(session, callback.from_user.id)
    if metrics:
        water_status = "✅" if metrics['water_glasses'] >= category['water'] else "❌"
        sleep_status = "✅" if metrics['sleep_hours'] >= category['hours'] else "❌"
        steps_status = "✅" if metrics['steps'] >= category['steps'] else "❌"
        text = f"📊 Твои показатели за сегодня:\n\n{water_status} Вода: {metrics['water_glasses']}/{category['water']} стаканов\n{sleep_status} Сон: {metrics['sleep_hours']}/{category['hours']} часов\n{steps_status} Шаги: {metrics['steps']}/{category['steps']}\n\nДата: {metrics['date']}"
    else:
        text = f"У тебя ещё нет данных за сегодня. 📝\n\nТвои цели:\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}"
    await callback.message.answer(text, reply_markup=kb.metrics_actions)

@health_router.callback_query(F.data == 'cancel_input')
async def cancel_input(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Ввод данных отменён. 🚫", reply_markup=kb.health)
    await callback.answer()

@health_router.callback_query(F.data == 'update_metrics_confirm')
async def update_metrics_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer('')
    category = await req_get_user_category(session, callback.from_user.id)
    await callback.message.answer(f"Введи новые данные:\n\nЦелевые показатели:\n💧 Вода: {category['water']} стаканов\n😴 Сон: {category['hours']} часов\n👣 Шаги: {category['steps']}\n\nВведи количество выпитых стаканов воды:", reply_markup=kb.cancel_keyboard)
    await state.set_state(MetricsStates.waiting_for_water)

@health_router.callback_query(F.data == 'back_to_health')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выбери категорию:', reply_markup=kb.health)

@health_router.callback_query(F.data == 'advice')
async def generate_advice(callback: CallbackQuery):
    await callback.answer('')
    random_adv = random.randint(1, 10)
    advice = ADVICES[random_adv]
    await callback.message.answer(advice, reply_markup=kb.back_to_heath)