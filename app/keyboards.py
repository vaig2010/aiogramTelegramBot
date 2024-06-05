from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/weather"),
            KeyboardButton(text="/site"),
        ],
        [
            KeyboardButton(text="/get_users"),
            KeyboardButton(text="/delete_users"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)