from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb

ID = None

# класс меню добавления букетов
class FSMbouquet(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

# получить права админа
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Введите команду', reply_markup=admin_kb.button_case_admin)
    await message.delete()



# начало диалога загрузки новой позиции в меню букетов
async def bouquet(message: types.Message):
    if message.from_user.id == ID:
        await  FSMbouquet.photo.set()
        await message.reply('Загрузите фото')

#Выход из состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

#первый ответ
async def load_photo(message:types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMbouquet.next()
        await message.reply('Введите название')

#Второй ответ
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
            await FSMbouquet.next()
            await message.reply('Введите описание')


#Третий ответ
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMbouquet.next()
        await message.reply('Укажите цену')

#Четвертый ответ
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()




def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(bouquet, commands=['Добавить_букет'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMbouquet.photo)
    dp.register_message_handler(load_name, state=FSMbouquet.name)
    dp.register_message_handler(load_description, state=FSMbouquet.description)
    dp.register_message_handler(load_price, state=FSMbouquet.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)


