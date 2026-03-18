from aiogram import F, Router, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
import logging as log

from ai.yandex_gpt import ask_yandex_gpt  
import keyboards.inline_kbd as kb

ai_router = Router()

skip_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⏭ Пропустить")]],
    resize_keyboard=True
)

confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Отправить")],
        [KeyboardButton(text="🔄 Заполнить заново")]
    ],
    resize_keyboard=True
)

# Класс состояний FSM
class HealthForm(StatesGroup):
    waiting_for_health = State()        
    waiting_for_psychological = State()  
    waiting_for_study = State()          
    confirmation = State()               

@ai_router.message(Command('conditions'))
async def cmd_health_message(message: Message, state: FSMContext):
    await message.answer(
        "🧠 **Оценка состояния**\n\n"
        "Я задам тебе несколько вопросов о твоем здоровье, психологическом состоянии и учебе.\n"
        "После этого нейросеть Yandex GPT даст тебе персональные рекомендации.\n\n"
        "Если не хочешь отвечать на какой-то вопрос, нажми 'Пропустить'.\n\n"
        "**Расскажи о своем физическом состоянии и активности:**\n"
        "(например: сколько спишь, занимаешься ли спортом, как питаешься)",
        reply_markup=skip_keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(HealthForm.waiting_for_health)

@ai_router.callback_query(F.data == 'conditions')
async def cmd_health_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(
        "🧠 **Оценка состояния**\n\n"
        "Я задам тебе несколько вопросов о твоем здоровье, психологическом состоянии и учебе.\n"
        "После этого нейросеть Yandex GPT даст тебе персональные рекомендации.\n\n"
        "Если не хочешь отвечать на какой-то вопрос, нажми 'Пропустить'.\n\n"
        "**Расскажи о своем физическом состоянии и активности:**\n"
        "(например: сколько спишь, занимаешься ли спортом, как питаешься)",
        reply_markup=skip_keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(HealthForm.waiting_for_health)

@ai_router.message(HealthForm.waiting_for_health)
async def process_health(message: Message, state: FSMContext):
    health_data = "Пропущено" if message.text == "⏭ Пропустить" else message.text
    await state.update_data(health=health_data)
    
    await message.answer(
        "🧘 **Психологическое состояние:**\n\n"
        "Расскажи о своем настроении, уровне стресса, качестве сна:\n"
        "(например: чувствую тревогу, плохо сплю, часто нервничаю)",
        reply_markup=skip_keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(HealthForm.waiting_for_psychological)

@ai_router.message(HealthForm.waiting_for_psychological)
async def process_psychological(message: Message, state: FSMContext):
    psychological_data = "Пропущено" if message.text == "⏭ Пропустить" else message.text
    await state.update_data(psychological=psychological_data)
    
    await message.answer(
        "📚 **Учеба:**\n\n"
        "Расскажи об учебе: нагрузка, успеваемость, мотивация:\n"
        "(например: много домашки, ничего не успеваю, сложно учиться)",
        reply_markup=skip_keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(HealthForm.waiting_for_study)

@ai_router.message(HealthForm.waiting_for_study)
async def process_study(message: Message, state: FSMContext):
    study_data = "Пропущено" if message.text == "⏭ Пропустить" else message.text
    await state.update_data(study=study_data)
    
    data = await state.get_data()
    
    summary = (
        f"📊 **Вот что ты рассказал(а):**\n\n"
        f"🏃 **Здоровье/активность:**\n{data['health']}\n\n"
        f"🧠 **Психологическое состояние:**\n{data['psychological']}\n\n"
        f"📚 **Учеба:**\n{data['study']}\n\n"
        f"Всё верно?"
    )
    
    await message.answer(summary, reply_markup=confirm_keyboard, parse_mode="Markdown")
    await state.set_state(HealthForm.confirmation)

@ai_router.message(HealthForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext, bot: Bot):
    if message.text == "✅ Отправить":
        status_msg = await message.answer(
            "🔍 **Анализирую данные и готовлю рекомендации...**\n"
            "Это займет несколько секунд.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        
        data = await state.get_data()
        
        try:
            await bot.send_chat_action(message.chat.id, action="typing")
            
            recommendation = await ask_yandex_gpt(
                data.get('health', ''),
                data.get('psychological', ''),
                data.get('study', '')
            )

            await status_msg.delete()
            
            if recommendation:
                await message.answer(
                    f"🤖 **Рекомендации от Yandex GPT:**\n\n{recommendation}",
                    parse_mode="Markdown",
                    reply_markup=kb.back_to_main_menu
                )
            else:
                await message.answer(
                    "❌ Не удалось получить рекомендации от нейросети.\n",
                    reply_markup=ReplyKeyboardRemove()
                )
            
        except Exception as e:
            log.error(f"Ошибка в GPT: {e}")
            await status_msg.delete()
            await message.answer(
                "❌ Произошла ошибка при получении рекомендаций.\n"
                "Попробуй еще раз через команду /conditions",
                reply_markup=ReplyKeyboardRemove()
            )
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/conditions")]],
            resize_keyboard=True
        )
        await message.answer(
            "Хочешь получить новые рекомендации? Нажми кнопку ниже:",
            reply_markup=keyboard
        )
        

        await state.clear()
        
    elif message.text == "🔄 Заполнить заново":
        await message.answer(
            "🔄 **Давай начнем сначала.**\n\n"
            "Расскажи о своем физическом состоянии:",
            reply_markup=skip_keyboard,
            parse_mode="Markdown"
        )
        await state.set_state(HealthForm.waiting_for_health)
    else:
        await message.answer("Пожалуйста, используй кнопки ниже")

@ai_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        "❌ Опрос отменен. Чтобы начать заново, используй /conditions",
        reply_markup=ReplyKeyboardRemove()
    )