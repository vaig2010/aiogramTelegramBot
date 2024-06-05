from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
import webbrowser
import weatherController

import app.keyboards as kb

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50))')
    conn.commit()
    cur.execute('INSERT INTO users(name) VALUES(?)', (message.from_user.first_name,))
    conn.commit()
    cur.close()
    conn.close()
    #await bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!")
    await message.answer(f"Hello {message.from_user.first_name}!", reply_markup=kb.main)

@router.message(Command('get_users'))
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
    
@router.message(Command('delete_users'))
async def delete_users(message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('DELETE FROM users')
    conn.commit()
    cur.close()
    conn.close()
    await message.answer( f"all users deleted")
    

class ChooseCity(StatesGroup):
    city = State()
    
@router.message(Command('weather'))
async def get_weather(message: Message, state: FSMContext):
    await message.answer("Enter city")
    await state.set_state(ChooseCity.city)

@router.message(ChooseCity.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    city = message.text.strip()
    weather = weatherController.getCityWeather(city)
    if weather is not None:
        icon_url = f"https://{weather['icon'][2:]}"
        await message.answer_photo(photo=icon_url, caption=f"{weather['city']}\n{weather['temperature']} °C\n{weather['description']}")
    else:
        await message.answer("City not found")
    await state.clear()
    
@router.message(Command('site'))
async def main(message):
    msg = message.text
    if " " in msg:
        msg = msg.split()[1]
    else:
        msg = "google.com"
    webbrowser.open(f"https://{msg}")

@router.message()
async def info(message):
    if message.text == "id":
        await message.answer(f"{message.from_user.id}")
    if message.text == "info":
        await message.answer(f"{message}")