import json
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery ,FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton 
from aiogram.methods import SendMediaGroup
from aiogram.types import InputMediaPhoto
from states1 import Newmember 
import buttons
from states1 import Change 
TOKEN = "do not copy!"


# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()

# Функция для загрузки данных из JSON файла [users.json]
def load_data():
    try:
        with open('users.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open('users.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



# Функция для загрузки данных из JSON файла [afisha.json]
def load_data1():
    try:
        with open('afisha.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {'user_ids': [], 'length': 0}  # Создаем новый словарь с начальными значениями
    return data

def save_data1(data):
    with open('afisha.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Функция для добавления нового пользователя в афишу
def add_user_to_afisha(user_id):
    data = load_data1()
    if user_id not in data['user_ids']:
        data['user_ids'].append(user_id)  # Добавляем нового пользователя
        data['length'] = len(data['user_ids'])  # Обновляем количество пользователей
        save_data1(data)
        return True
    return False

# Функция для удаления пользователя из афиши
def remove_user_from_afisha(user_id):
    data = load_data1()
    if user_id in data['user_ids']:
        data['user_ids'].remove(user_id)  # Удаляем пользователя
        data['length'] = len(data['user_ids'])  # Обновляем количество пользователей
        save_data1(data)
        return True
    return False



#CommandStart 

@dp.message(Command("start"))
async def start(message: Message):
    data1 = load_data()
    if str(message.from_user.id) in data1:
        await message.answer("Неизвестная команда")
    else:
        await message.answer(f"Привет <b>{message.from_user.first_name}</b> ! \nЗдесь играют в мафию\nНаши клубы есть в этих городах, пожалуйста, выбери свой",parse_mode="HTML",reply_markup=buttons.cities)
    
#Команда правила 
@dp.message(Command("rules"))
async def pravila(message: Message):
    await message.answer("https://www.youtube.com/watch?v=AUhRHtx3Rbc&feature=youtu.be")

#Сама команда афиши , где выбираешь событие 
@dp.message(Command("afisha"))
async def mainafisha(message: Message):
    usid = message.from_user.id
    data = load_data()
    if str(usid) in data:
        await message.answer(f"""<b>Имя</b> - <i>{data[str(usid)]['name']}</i> 
    Самое время начать! Вот список игр, выбирай, когда удобно, и записывайся!
    """,parse_mode="HTML",reply_markup=buttons.afishaoptions)
    else:
        await message.answer("У вас еще нет профиля , зарегистрируйтесь и записывайтесь на все наши игры.")

#Самое действие , само бронирование и осмотр ресторанов!
@dp.callback_query(lambda callback_query: callback_query.data == "mainevent")
async def getin(callback: CallbackQuery, state: FSMContext):
    zap = buttons.generate_keyboard()
    photo_id = "AgACAgIAAxkBAAIBYWYSmVuq-U5NhUhKAtO-aG1bMDnCAAKl2TEbi1-RSFdyua2d9NHGAQADAgADeQADNAQ"
    await callback.message.answer_photo(photo_id,"""Друзья! ❤️‍🔥

В Среду 10.04 играем в ресторане  One Lounge | Restaurant

Адрес: 5648 International Dr

(Все интересующие вопросы можно задавать в нашем мафиозном чате: https://t.me/Mafia_Orlando_Game

 Начало в 07.00 ✔️

 Стоимость: 35$ с человека за весь вечер игр✅
""",reply_markup=zap)
    

#callback бронирования
@dp.callback_query(lambda callback_query: callback_query.data == "getin")
async def getin(callback: CallbackQuery, state: FSMContext):
    final_num1 = 20
    data = load_data1()
    if callback.from_user.id in data["user_ids"]:
        await callback.message.answer("Вы уже забронировали!")
    elif callback.from_user.id not in data["user_ids"] and data["length"]<final_num1:
        add_user_to_afisha(callback.from_user.id)
        await callback.message.answer("Вы забронировали слот, поздравляем!")
    else:
        await callback.message.answer("Извините но все слоты уже заняты , нам безумно жаль!")

@dp.callback_query(lambda callback_query: callback_query.data == "allplayers")
async def allplayers(callback: CallbackQuery, state: FSMContext): 
    media_group = []
    afisha_data = load_data1()  # Загрузить данные из JSON файла afisha.json
    users_data = load_data()  # Загрузить данные из JSON файла users.json
    user_counter = 1
    # Сначала отправляем имена пользователей с нумерацией
    message_text = ""

    # Сначала добавляем имена пользователей с нумерацией к тексту
    for user_id in afisha_data['user_ids']:
        user_info = users_data.get(str(user_id))  # Получить информацию о пользователе из users.json
        
        if user_info:
            name = user_info.get('name', '')
            # Добавляем номер перед именем пользователя к тексту
            message_text += f"{user_counter}. {name}\n"
            user_counter += 1
    
    # Отправляем текст с нумерацией и именами пользователей
    await callback.message.answer(message_text)

        
    # Затем отправляем фотографии пользователей
    for user_id in afisha_data['user_ids']:
        user_info = users_data.get(str(user_id))  # Получить информацию о пользователе из users.json
        
        if user_info:
            avatar_id = user_info.get('avatar_id', '')
            if avatar_id:
                media_group.append(InputMediaPhoto(media=avatar_id))
    
    if media_group:
        await bot.send_media_group(chat_id=callback.from_user.id,media=media_group)
                



# Убрать броньку GETOFF
@dp.callback_query(lambda callback_query: callback_query.data == "getoff")
async def getoff(callback: CallbackQuery, state: FSMContext):
    data = load_data1()
    if callback.from_user.id not in data["user_ids"]:
        await callback.message.answer("Вы пока что не бронировали слот. Самое время забронировать!")
    elif callback.from_user.id in data["user_ids"]:
        remove_user_from_afisha(callback.from_user.id)
        await callback.message.answer("Вы убрали слот!")
        


#await bot.send_photo(chat_id=callback.from_user.id, photo=avatar_id)
    


# Команда /профиль 
@dp.message(Command("profile"))
async def start(message: Message):
    data1 = load_data()
    await message.answer("Можешь посмотреть и отредактировать профиль здесь")
    await message.answer_photo(data1[str(message.from_user.id)]["avatar_id" ])
    await message.answer(f"""Профиль

<b>Имя</b>: {data1[str(message.from_user.id)]["name"]}
<b>Номер телефона</b>: {data1[str(message.from_user.id)]["phone_number"]}
""",parse_mode="HTML")
    await message.answer("Все верно?",reply_markup=buttons.vseverno)


#callbacks PROFILE NET NET NET NET NET NET NET NET NET NET NET NET NET 
@dp.callback_query(lambda callback_query: callback_query.data == "net")
async def no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Ок, что будем редактировать?",reply_markup=buttons.options)
#Callback Name 
@dp.callback_query(lambda callback_query: callback_query.data == "name")
async def no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи Имя")
    await state.set_state(Change.Namenew)

@dp.message(Change.Namenew)
async def getnewname(message: Message,state: FSMContext):
    data = load_data()
    newname = message.text
    data[str(message.from_user.id)]['name'] = newname
    save_data(data)
    await message.answer_photo(data[str(message.from_user.id)]["avatar_id" ])
    await message.answer(f"""Профиль

<b>Имя</b>: {data[str(message.from_user.id)]["name"]}
<b>Номер телефона</b>: {data[str(message.from_user.id)]["phone_number"]}
""",parse_mode="HTML")
    await message.answer("Все верно?",reply_markup=buttons.vseverno)
    await state.clear()

#Callback Number 
@dp.callback_query(lambda callback_query: callback_query.data == "number")
async def no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи номер")
    await state.set_state(Change.Numbernew)

@dp.message(Change.Numbernew)
async def getnewname(message: Message,state: FSMContext):
    data = load_data()
    newnumber = message.text
    data[str(message.from_user.id)]['phone_number'] = newnumber
    save_data(data)
    await message.answer_photo(data[str(message.from_user.id)]["avatar_id" ])
    await message.answer(f"""Профиль

<b>Имя</b>: {data[str(message.from_user.id)]["name"]}
<b>Номер телефона</b>: {data[str(message.from_user.id)]["phone_number"]}
""",parse_mode="HTML")
    await message.answer("Все верно?",reply_markup=buttons.vseverno)
    await state.clear()
    


#Callback Avatar
@dp.callback_query(lambda callback_query: callback_query.data == "avatarid")
async def no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправь фотку")
    await state.set_state(Change.Avatarnew)

@dp.message(Change.Avatarnew, F.photo)
async def getnewname(message: Message,state: FSMContext):
    data = load_data()
    newavatar = message.photo[-1].file_id
    data[str(message.from_user.id)]['avatar_id'] = newavatar
    save_data(data)
    await message.answer_photo(data[str(message.from_user.id)]["avatar_id" ])
    await message.answer(f"""Профиль

<b>Имя</b>: {data[str(message.from_user.id)]["name"]}
<b>Номер телефона</b>: {data[str(message.from_user.id)]["phone_number"]}
""",parse_mode="HTML")
    await message.answer("Все верно?",reply_markup=buttons.vseverno)
    await state.clear()
#callbacks PROFILE DA DA DA DA DA DA DA DA DA DA DA DA DA 
@dp.callback_query(lambda callback_query: callback_query.data == "yes")
async def yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отлично!")

#callbacks NEW YORK
@dp.callback_query(lambda callback_query: callback_query.data == "ny")
async def ny(callback: CallbackQuery, state: FSMContext):
    data = load_data()
    if str(callback.from_user.id) in data:
        await callback.message.answer("Неизвестная команда вы уже зарегистрированы!")
    else:
        await callback.message.answer("NEW YORK, отлично!")
        await callback.message.answer("С городом разобрались, теперь подскажи, как тебя зовут?")
        await state.set_state(Newmember.Name)

@dp.message(Newmember.Name)
async def getname(message: Message , state: FSMContext):
    await state.update_data(Name=message.text)
    await state.set_state(Newmember.Number)
    await message.answer("Введите номер телефона!")

@dp.message(Newmember.Number)
async def getnum(message: Message, state: FSMContext):
    await state.update_data(Number=message.text)
    await state.set_state(Newmember.Avatar)
    await message.answer("Осталось только загрузить вашу аватарку.Отправьте ваш аватар.")

@dp.message(Newmember.Avatar , F.photo)
async def getavatar(message: Message, state: FSMContext):
    user_id = message.from_user.id
    avatar_id = message.photo[-1].file_id
    data = await state.get_data()
    name = data["Name"]
    await state.clear()
    await message.answer("""Отлично, в таком случае регистрация завершена 🔥🔥🔥\nВыбери в меню пункт "Афиши" чтобы посмотреть запланированные игры""")
    data1 = load_data()

    # Добавляем информацию о новом пользователе в словарь данных
    data1[str(user_id)] = {
        "name": str(name),
        "phone_number": data["Number"],
        "avatar_id": avatar_id
    }

    # Сохраняем обновленные данные в JSON файл
    save_data(data1)

    
    














async def main() -> None:
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
