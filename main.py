import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import webbrowser
import sqlite3
import requests
import keys
import weatherController

bot_key = keys.bot_key
bot = Bot(bot_key)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
    
class ChoseCountry(StatesGroup):
    choosing_country_name = State()
    
@dp.message(Command('start'))
async def start(message: types.Message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50))')
    conn.commit()
    cur.execute('INSERT INTO users(name) VALUES(?)', (message.from_user.first_name,))
    conn.commit()
    cur.close()
    conn.close()
    #await bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!")
    await message.answer(f"Hello {message.from_user.first_name}!")

@dp.message(Command('get_users'))
async def get_users(message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('SELECT name FROM users')
    users = cur.fetchall()
    all_users = ""
    for user in users:
        all_users += f"{user[0]}\n"
    cur.close()
    conn.close()
    if all_users == "":
        await message.answer(f"no users")
    else:
        await message.answer(f"{all_users}")
    
@dp.message(Command('delete_users'))
async def delete_users(message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('DELETE FROM users')
    conn.commit()
    cur.close()
    conn.close()
    await message.answer( f"all users deleted")
    

@router.message(Command('weather'), StateFilter(None))
async def get_weather(message: types.Message, state: FSMContext):
    await message.answer("Enter city")
    await state.set_state(ChoseCountry.choosing_country_name)

@router.message(StateFilter(ChoseCountry.choosing_country_name))
async def get_city(message: types.Message, state: FSMContext):
    city = message.text.strip()
    weather = weatherController.getCityWeather(city)
    if weather is not None:
        icon_url = f"https://{weather['icon'][2:]}"
        await message.answer_photo(photo=icon_url, caption=f"{weather['city']}\n{weather['temperature']} °C\n{weather['description']}")
    else:
        await message.answer("City not found")
    await state.clear()
    
@dp.message(Command('site'))
async def main(message):
    msg = message.text
    if " " in msg:
        msg = msg.split()[1]
    else:
        msg = "google.com"
    webbrowser.open(f"https://{msg}")

@dp.message()
async def info(message):
    if message.text == "id":
        await message.answer(f"{message.from_user.id}")
    if message.text == "info":
        await message.answer(f"{message}")
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())