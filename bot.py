import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. LOGGING VA SOZLAMALAR
logging.basicConfig(level=logging.INFO)

# Tokenni Render'dagi Environment Variable'dan o'qiydi (Xavfsiz va to'g'ri yo'l)
BOT_TOKEN = os.getenv("BOT_TOKEN") 
ADMIN_USERNAME = "U_Z_BxG"
NETLIFY_URL = "https://haxi-agency.netlify.app" # O'zingizning Netlify linklingizni kiriting

if not BOT_TOKEN:
    exit("Xatolik: BOT_TOKEN muhit o'zgaruvchisi topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 2. TUGMALAR (KLAVIATURA)
def get_main_menu():
    kb = [
        [
            types.KeyboardButton(text="📂 Xizmatlar ko'rsatish"),
            types.KeyboardButton(text="📊 Statistika & Kafolat")
        ],
        [
            types.KeyboardButton(text="🌐 Bizning Sayt (Web App)"),
            types.KeyboardButton(text="📞 Aloqa & Hamkorlik")
        ]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Telegram Bot ($140 dan)", callback_data="serv_bot")],
        [InlineKeyboardButton(text="🌐 Veb-Sayt ($200 dan)", callback_data="serv_web")],
        [InlineKeyboardButton(text="🎬 AI Video Kliplar ($100 dan)", callback_data="serv_video")],
        [InlineKeyboardButton(text="✨ Ijtimoiy Tarmoqlar ($70 dan)", callback_data="serv_smm")]
    ])

def get_order_keyboard(service_name):
    text_msg = f"Assalomu alaykum, men premium {service_name} xizmatini buyurtma qilmoqchi edim."
    encoded_text = text_msg.replace(" ", "%20")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Buyurtma berish (Telegram)", url=f"https://t.me/{ADMIN_USERNAME}?text={encoded_text}")],
        [InlineKeyboardButton(text="⬅️ Xizmatlarga qaytish", callback_data="back_to_services")]
    ])

# 3. HANDLERS (REAKSIYALAR)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "⚡ **HAXI AGENCY Telegram Botiga Xush Kelibsiz!**\n\n"
        "Biz biznesingiz uchun premium darajadagi yuqori texnologik va sun'iy intellekt (AI) "
        "yechimlarini taklif etamiz. Menyudan foydalanib xizmatlarimiz bilan tanishing."
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

@dp.message(F.text == "📂 Xizmatlar ko'rsatish")
async def show_services(message: types.Message):
    await message.answer("👇 **Kerakli kiber-ekosistema xizmatini tanlang:**", parse_mode="Markdown", reply_markup=get_services_keyboard())

@dp.message(F.text == "📊 Statistika & Kafolat")
async def show_stats(message: types.Message):
    stats_text = (
        "⚡ **HAXI AGENCY Eksklyuziv Ko'rsatkichlari:**\n\n"
        "🌐 **5+ Yil** — Professional tajriba\n"
        "👥 **200+** — Mamnun mijozlar\n"
        "🚀 **200+** — Muvaffaqiyatli yakunlangan loyihalar\n"
        "🏆 **100%** — Sifat va xavfsizlik kafolati"
    )
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message(F.text == "📞 Aloqa & Hamkorlik")
async def show_contact(message: types.Message):
    contact_text = f"✨ G'oya va takliflaringiz bo'lsa, to'g'ridan-to'g'ri adminga murojaat qiling: @{ADMIN_USERNAME}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Suhbat boshlash", url=f"https://t.me/{ADMIN_USERNAME}")]
    ])
    await message.answer(contact_text, parse_mode="Markdown", reply_markup=kb)

@dp.message(F.text == "🌐 Bizning Sayt (Web App)")
async def show_webapp(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Saytni Bot Ichida Ochish", web_app=WebAppInfo(url=NETLIFY_URL))]
    ])
    await message.answer("Premium interfeysga ega saytimizni to'g'ridan-to'g'ri bot ichida ko'ring:", reply_markup=kb)

# 4. CALLBACKS
@dp.callback_query(F.data.startswith("serv_"))
async def process_service_click(callback: types.CallbackQuery):
    service = callback.data.split("_")[1]
    if service == "bot":
        txt = "🤖 **Telegram Bot Xizmati**\n\nBiznes jarayonlarni to'liq avtomatlashtiruvchi, xatosiz va AI bilan jihozlangan premium botlar.\n\n💰 **Narxi:** $140 dan"
        name = "Telegram Bot"
    elif service == "web":
        txt = "🌐 **Veb-Sayt & SaaS**\n\nO'ta tez chiquvchi, premium UI/UX dizaynli, zamonaviy SaaS va Landing Page platformalari.\n\n💰 **Narxi:** $200 dan"
        name = "Veb-Sayt"
    elif service == "video":
        txt = "🎬 **AI Video Kliplar**\n\nNeyrotarmoqlar yordamida kinematografik reklama roliklari va kreativ animatsiyalar yaratish.\n\n💰 **Narxi:** $100 dan"
        name = "AI Video Kliplar"
    elif service == "smm":
        txt = "✨ **Ijtimoiy Tarmoqlar (SMM & SEO)**\n\nYouTube va Telegram uchun AI mualliflik dizaynlari, musiqalar va professional SEO xizmati.\n\n💰 **Narxi:** $70 dan"
        name = "Ijtimoiy Tarmoqlar"

    await callback.message.edit_text(txt, parse_mode="Markdown", reply_markup=get_order_keyboard(name))
    await callback.answer()

@dp.callback_query(F.data == "back_to_services")
async def back_services(callback: types.CallbackQuery):
    await callback.message.edit_text("👇 **Kerakli kiber-ekosistema xizmatini tanlang:**", parse_mode="Markdown", reply_markup=get_services_keyboard())
    await callback.answer()

# 5. ISHGA TUSHIRISH (RENDER UCHUN OPTIMALLASHGAN)
async def main():
    # Eski oqimlarni tozalaydi, bot ikki marta javob bermaydi
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
