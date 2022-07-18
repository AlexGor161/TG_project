from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db


async  def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Флористический салон №1', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через лс, напишите ему:\nhttps://t.me/bcquotes_bot')


async  def open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пионы\nРозы\nТюльпаны\nБукеты\nЦветы в коробке')


async  def place_comnand(message: types.Message):
    await bot.send_message(message.from_user.id, 'г. Ростов-на-Дону, ул. Большая садовая д. 35\nтел.:8988-777-77-77')


async def kind_bouquet(message: types.Message):
    await sqlite_db.sql_read(message)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(open_command, lambda message: 'ассортимент' in message.text)
    dp.register_message_handler(place_comnand, lambda message: 'контакты' in message.text)
    dp.register_message_handler(kind_bouquet, lambda message: 'букеты' in message.text)