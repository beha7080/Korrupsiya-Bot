import logging
from databace import conn, cursor
from states import *
from config import WEB_APP_URL
from aiogram import Bot, Dispatcher, types
from Keyboards.default import menu_button, star_button
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Salom, {message.from_user.full_name}! Botimizga xush kelibsiz.', reply_markup=menu_button)


@dp.message_handler(text='📝 Korruptsiya haqida xabar berish')
async def report_corruption(message: types.Message):
    await message.answer(
        'Iltimos, korruptsiya haqida ma\'lumotni kiriting. Sizning xabaringiz ma\'lumotlar bazasida saqlanadi.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Form.waiting_for_report.set()


@dp.message_handler(text='📚 Hisobotlarni ko‘rish')
async def view_reports(message: types.Message):
    cursor.execute("SELECT report FROM reports WHERE user_id = ?", (message.from_user.id,))
    reports = cursor.fetchall()
    if reports:
        txt = 'Sizning Hisbotlaringiz\n\n'
        son = 0
        for i in reports:
            son += 1
            txt += f"""
{son}) {i[0]}             
            """
        txt += f'\n\nHisobotlar soni: {len(reports)}'
        await message.answer(txt)
    else:
        await message.answer('Sizning xabaringiz topilmadi ❌')
    await message.answer('Harakatni tanlang:', reply_markup=menu_button)


@dp.message_handler(text='📖 Ma\'lumot')
async def information(message: types.Message):
    info_text = """
Ushbu bot korruptsiya hisobotlarini to‘plash va ko‘rish uchun mo‘ljallangan.
Siz quyidagi imkoniyatlarga egasiz:
1. Korruptsiya haqida xabar berish
2. Barcha hisobotlarni ko‘rish
3. Bot haqida ma'lumot olish
Sizning hisobotlaringiz anonim tarzda saqlanadi va tekshiriladi."
    """
    await message.answer(info_text)


@dp.message_handler(text='⭐️ Baholang')
async def rate_us(message: types.Message):
    await message.answer(
        'Iltimos, bizni baholang, yulduzlar sonini tanlang:',
        reply_markup=star_button
    )
    await Form.waiting_for_rating.set()


@dp.message_handler(text=['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐'], state=Form.waiting_for_rating)
async def handle_rating(message: types.Message, state: FSMContext):
    ratings = {
        '⭐☆☆☆☆': 1,
        '⭐⭐☆☆☆': 2,
        '⭐⭐⭐☆☆': 3,
        '⭐⭐⭐⭐☆': 4,
        '⭐⭐⭐⭐⭐': 5
    }
    rating = ratings.get(message.text, 0)
    cursor.execute('INSERT INTO feedback (user_id, rating) VALUES (?, ?)', (message.from_user.id, rating))
    conn.commit()
    await message.answer('Baholaganingiz uchun rahmat!')
    await message.answer('Harakatni tanlang:', reply_markup=menu_button)
    await state.finish()


@dp.message_handler(text='📞 Call Center')
async def call_center(message: types.Message):
    contact_info = """
📞 **Call Center**
Agar sizda savollar bo‘lsa yoki bizning qo‘llab-quvvatlash xizmatimiz bilan bog‘lanmoqchi bo‘lsangiz, quyidagi aloqa ma'lumotlaridan foydalanishingiz mumkin
📧 Elektron pochta: tasmatovbehruz72@gmail.com
📞 Telefon: +998974917080
Sizga yordam berishdan doimo mamnunmiz!
    """
    await message.answer(contact_info)


@dp.message_handler(text='📰 R.uz maqolalari')
async def articles_r_uz(message: types.Message):
    await message.answer("""
📰 **R.uz maqolalari**
Siz R.uz saytida dolzarb maqolalar bilan tanishishingiz mumkin
[R.uz maqolalari](https://www.lex.uz/acts/111457)
Agar sizda savollar bo‘lsa yoki qo‘shimcha ma'lumot kerak bo‘lsa, iltimos, Call Center bilan bog‘laning
    """)


@dp.message_handler(text='📜 R.uz qonunlari')
async def laws_r_uz(message: types.Message):
    await message.answer("""
📜 **R.uz qonunlari**
Siz R.uz saytida dolzarb qonunlar bilan tanishishingiz mumkin:
[R.uz qonunlari](https://www.lex.uz/)
Agar sizda savollar bo‘lsa yoki qo‘shimcha ma'lumot kerak bo‘lsa, iltimos, Call Center bilan bog‘laning
        """)


@dp.message_handler(state=Form.waiting_for_report)
async def handle_message(message: types.Message, state: FSMContext):
    report = message.text
    cursor.execute('INSERT INTO reports (user_id, report) VALUES (?, ?)', (message.from_user.id, report))
    conn.commit()
    await message.answer('Sizning xabaringiz muvaffaqiyatli saqlandi.')
    await message.answer('Harakatni tanlang:', reply_markup=menu_button)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
