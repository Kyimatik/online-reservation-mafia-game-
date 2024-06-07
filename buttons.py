from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove

from gfderg import load_data1

cities = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="New York",callback_data="ny")
            
        ]
    ],
    resize_keyboard=True
)


vseverno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Нет, Отредактировать",callback_data="net"),
            InlineKeyboardButton(text="Да, Все ок",callback_data="yes")
        ]
    ],
    resize_keyboard=True
)


options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Имя",callback_data="name")
        ],
        [
            InlineKeyboardButton(text="Номер телефона",callback_data="number")
            
        ],
        [
            InlineKeyboardButton(text="Аватар",callback_data="avatarid")
        ]
    ],
    resize_keyboard=True
)

#  # Загрузка данных из файла
def generate_keyboard():
    final_num = 20
    data = load_data1()  # Загрузить данные
    zapiska = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"Игроки ({data['length']}/{final_num})", callback_data="allplayers")
            ],
            [
                InlineKeyboardButton(text="Записаться", callback_data="getin")
            ],
            [
                InlineKeyboardButton(text="Убрать бронь",callback_data="getoff")
            ]
            
        ],
        resize_keyboard=True
    )
    return zapiska


#Список игр Афиша
afishaoptions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мафия 08.05.2024/Disfrutar | Restraunt",callback_data="mainevent")
        ]
    ],
    resize_keyboard=True
)