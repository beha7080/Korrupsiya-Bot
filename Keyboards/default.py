from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo
from config import WEB_APP_URL

menu_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📝 Korruptsiya haqida xabar berish'),
            KeyboardButton(text='📚 Hisobotlarni ko‘rish')
        ],
        [
            KeyboardButton(text='📖 Ma\'lumot'),
            KeyboardButton(text='⭐️ Baholang')
        ],
        [
            KeyboardButton(text='📞 Call Center'),
            KeyboardButton(text='📰 R.uz maqolalari')
        ],
        [
            KeyboardButton(text='📜 R.uz qonunlari')
        ],
        [
            KeyboardButton('Web sahifani ochish',
                           web_app=WebAppInfo(url=WEB_APP_URL))
        ]
    ],
    resize_keyboard=True
)

star_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⭐☆☆☆☆'),
            KeyboardButton(text='⭐⭐☆☆☆'),
            KeyboardButton(text='⭐⭐⭐☆☆'),
            KeyboardButton(text='⭐⭐⭐⭐☆'),
            KeyboardButton(text='⭐⭐⭐⭐⭐')
        ]
    ],
    resize_keyboard=True
)
