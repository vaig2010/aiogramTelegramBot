import telebot
import webbrowser
import sqlite3
import requests
import keys
import weatherController

bot_key = keys.bot_key
bot = telebot.TeleBot(bot_key)
    
@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50))')
    conn.commit()
    cur.execute('INSERT INTO users(name) VALUES(?)', (message.from_user.first_name,))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!")

@bot.message_handler(commands=['get_users'])
def get_users(message):
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
        bot.send_message(message.chat.id, f"no users")
    else:
        bot.send_message(message.chat.id, f"{all_users}")
    
@bot.message_handler(commands=['delete_users'])
def delete_users(message):
    conn = sqlite3.connect("aiogram.sqlite3")
    cur = conn.cursor()
    cur.execute('DELETE FROM users')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f"all users deleted")
    
@bot.message_handler(commands=['weather'])
def get_weather(message):
    bot.send_message(message.chat.id, "Enter city")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    city = message.text.strip()
    weather = weatherController.getCityWeather(city)
    if weather is not None:
        icon = weather['icon'][2:] # idk why it starts with "//"
        bot.send_photo(message.chat.id, caption=f"{weather['city']}\n{weather['temperature']} C\n{weather['description']}", photo=icon)
    else:
        bot.send_message(message.chat.id, "City not found")
    
@bot.message_handler(commands=['site'])
def main(message):
    msg = message.text
    if " " in msg:
        msg = msg.split()[1]
    else:
        msg = "google.com"
    webbrowser.open(f"https://{msg}")

@bot.message_handler()
def info(message):
    if message.text == "id":
        bot.send_message(message.chat.id, f"{message.from_user.id}")
    if message.text == "info":
        bot.send_message(message.chat.id, f"{message}")
        
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, "ok")
    
    
bot.polling(none_stop=True)