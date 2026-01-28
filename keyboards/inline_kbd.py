from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

psychology = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆘 SOS (антистресс)', callback_data='sos')],
    [InlineKeyboardButton(text='📖 Дневник настроения', callback_data='happy_diary')],
    [InlineKeyboardButton(text='🧭 Навигатор помощи', callback_data='help_navig')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')],
])

sos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣', callback_data='soss_1')],
    [InlineKeyboardButton(text='2️⃣', callback_data='soss_2')],
    [InlineKeyboardButton(text='3️⃣', callback_data='soss_3')],
    [InlineKeyboardButton(text='4️⃣', callback_data='soss_4')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

back_to_sos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='sos')],
])

mood_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='😊 Отлично', callback_data='mood_happy')],
    [InlineKeyboardButton(text='🙂 Хорошо', callback_data='mood_good')],
    [InlineKeyboardButton(text='😐 Нормально', callback_data='mood_neutral')],
    [InlineKeyboardButton(text='😔 Плохо', callback_data='mood_sad')],
    [InlineKeyboardButton(text='😤 Ужасно', callback_data='mood_angry')],
    [InlineKeyboardButton(text='📊 Моя статистика', callback_data='mood_stats')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

mood_stats_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить настроение', callback_data='happy_diary')],
    [InlineKeyboardButton(text='⬅️ Назад к выбору', callback_data='happy_diary')],
])

problems = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣', callback_data='problem_1')],
    [InlineKeyboardButton(text='2️⃣', callback_data='problem_2')],
    [InlineKeyboardButton(text='3️⃣', callback_data='problem_3')],
    [InlineKeyboardButton(text='4️⃣', callback_data='problem_4')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='psychology')],
])

back_to_navigator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='help_navig')],
])

learning_kb = get_callback_btns(btns={
    '📝 Добавить ДЗ': 'addhomework',
    '📚 Мои ДЗ': 'my_homeworks',
    '📊 Мой прогресс': 'my_progress',
    '💡 Получить совет': 'get_an_advice',
    '⬅️ Назад в меню': 'back_to_main_menu',
})

hw_back_cancel_kb = get_callback_btns(btns={
    '↩️ Назад': 'back',
    '❌ Отмена': 'cancel',
})