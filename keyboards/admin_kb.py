from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



#кнопки клавиатуры админа
button_load = KeyboardButton('Добавить букет')
button_delete = KeyboardButton('Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .add(button_delete)