from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

back_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')],
])

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

health = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💡 Совет', callback_data='advice')],
    [InlineKeyboardButton(text='📝 Показатели', callback_data='categories')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')],
])

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_input')]
])

update_metrics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да, обновить', callback_data='update_metrics_confirm')],
    [InlineKeyboardButton(text='❌ Нет, оставить как есть', callback_data='health')]
])

back_to_heath = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='health')]
])

metrics_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Обновить данные', callback_data='categories')],
    [InlineKeyboardButton(text='📈 Статистика', callback_data='stats')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='health')]
])

hobbies = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Спортивные занятия', callback_data='sports')],
    [InlineKeyboardButton(text='Интеллектуальные хобби', callback_data='iq')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_main_menu')]
])

sports = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚽️ Футбол', callback_data='s_football')],
    [InlineKeyboardButton(text='🏐 Воллейбол', callback_data='s_volleyball')],
    [InlineKeyboardButton(text='🏀 Баскетбол', callback_data='s_basketball')],
    [InlineKeyboardButton(text='🏒 Хоккей', callback_data='s_hockey')],
    [InlineKeyboardButton(text='🥊 Бокс', callback_data='s_box')],
    [InlineKeyboardButton(text='🤸‍♀️ Гимнастика', callback_data='s_gymnastick')],
    [InlineKeyboardButton(text='⛸️ Фигурное катание', callback_data='s_ice_skating')],
    [InlineKeyboardButton(text='🎾Теннис', callback_data='s_tennis')],
    [InlineKeyboardButton(text='🏊‍♂️ Плавание', callback_data='s_swimming')],
    [InlineKeyboardButton(text='🤼 Борьба', callback_data='s_wrestling')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='hobbies')]
])

iq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♟️ Шахматы', callback_data='iq_chess')],
    [InlineKeyboardButton(text='💻 Программирование', callback_data='iq_it')],
    [InlineKeyboardButton(text='🎮 Киберспорт', callback_data='iq_gaming')],
    [InlineKeyboardButton(text='🧩 Пазлы', callback_data='iq_puzzles')],
    [InlineKeyboardButton(text='🧶 Вязание / Плетение из бисера', callback_data='iq_knit')],
    [InlineKeyboardButton(text='🎨 Рисование', callback_data='iq_drawing')],
    [InlineKeyboardButton(text='🧱 Лепка (из глины, пластилина)', callback_data='iq_modelling')],
    [InlineKeyboardButton(text='🔢 Решение судоку', callback_data='iq_sudoku')],
    [InlineKeyboardButton(text='✍️ Решение кроссвордов', callback_data='iq_crosswords')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='hobbies')]
])