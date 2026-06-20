import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("8710679355:AAHUw2KQsliPl-IynoEgkMoFLs6ebKmW020")
ADMIN_USERNAME = "U_Z_BxG"
NETLIFY_URL = "https://haxi-agency.netlify.app"

if not BOT_TOKEN:
    exit("Xatolik: BOT_TOKEN topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# TUGMALAR
def get_main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📂 Xizmatlar ko'rsatish", "📊 Statistika & Kafolat")
    kb.row("🌐 Bizning Sayt (Web App)", "📞 Aloqa & Hamkorlik")
    return kb

def get_services_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🤖 Telegram Bot ($140 dan)", callback_data="serv_bot"),
        InlineKeyboardButton("🌐 Veb-Sayt ($200 dan)", callback_data="serv_web"),
        InlineKeyboardButton("🎬 AI Video Kliplar ($100 dan)", callback_data="serv_video"),
        InlineKeyboardButton("✨ Ijtimoiy Tarmoqlar ($70 dan)", callback_data="serv_smm")
    )
    return kb

def get_order_keyboard(service_name):
    text_msg = f"Assalomu alaykum, men premium {service_name} xizmatini buyurtma qilmoqchi edim."
    encoded_text = text_msg.replace(" ", "%20")
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🚀 Buyurtma berish (Telegram)", url=f"https://t.me/{ADMIN_USERNAME}?text={encoded_text}"),
        InlineKeyboardButton("⬅️ Xizmatlarga qaytish", callback_data="back_to_services")
    )
    return kb

# HANDLERS
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("⚡ **HAXI AGENCY Telegram Botiga Xush Kelibsiz!**\n\nBiznesingiz uchun premium AI yechimlarni taklif etamiz.", parse_mode="Markdown", reply_markup=get_main_menu())

@dp.message_handler(lambda message: message.text == "📂 Xizmatlar ko'rsatish")
async def show_services(message: types.Message):
    await message.answer("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())

@dp.message_handler(lambda message: message.text == "📊 Statistika & Kafolat")
async def show_stats(message: types.Message):
    stats_text = "⚡ **HAXI AGENCY:**\n\n🌐 **5+ Yil** — Tajriba\n👥 **200+** — Mijozlar\n🚀 **200+** — Loyihalar\n🏆 **100%** — Kafolat"
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "📞 Aloqa & Hamkorlik")
async def show_contact(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("💬 Suhbat boshlash", url=f"https://t.me/{ADMIN_USERNAME}"))
    await message.answer(f"✨ Adminga murojaat qiling: @{ADMIN_USERNAME}", reply_markup=kb)

@dp.message_handler(lambda message: message.text == "🌐 Bizning Sayt (Web App)")
async def show_webapp(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("💻 Saytni Ochish", web_app=WebAppInfo(url=NETLIFY_URL)))
    await message.answer("Premium saytimizni bot ichida ko'ring:", reply_markup=kb)

@dp.callback_query_handler(lambda call: call.data.startswith("serv_"))
async def process_service_click(call: types.CallbackQuery):
    service = call.data.split("_")[1]
    titles = {"bot": ["Telegram Bot", "$140 dan"], "web": ["Veb-Sayt", "$200 dan"], "video": ["AI Video Kliplar", "$100 dan"], "smm": ["Ijtimoiy Tarmoqlar", "$70 dan"]}
    txt = f"🤖 **{titles[service][0]} Xizmati**\n\nPremium va kiber-yechimlar.\n\n💰 **Narxi:** {titles[service][1]}"
    await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=get_order_keyboard(titles[service][0]))
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == "back_to_services")
async def back_services(call: types.CallbackQuery):
    await call.message.edit_text("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
