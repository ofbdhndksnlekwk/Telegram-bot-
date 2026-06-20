import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("8710679355:AAHUw2KQsliPl-IynoEgkMoFLs6ebKmW020") 
ADMIN_USERNAME = "U_Z_BxG"
NETLIFY_URL = "https://haxi-agency.netlify.app"

if not BOT_TOKEN:
    exit("Xatolik: BOT_TOKEN topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# TUGMALAR
def get_main_menu():
    kb = [
        [types.KeyboardButton(text="📂 Xizmatlar ko'rsatish"), types.KeyboardButton(text="📊 Statistika & Kafolat")],
        [types.KeyboardButton(text="🌐 Bizning Sayt (Web App)"), types.KeyboardButton(text="📞 Aloqa & Hamkorlik")]
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

# HANDLERS
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("⚡ **HAXI AGENCY Telegram Botiga Xush Kelibsiz!**\n\nBiznesingiz uchun premium AI yechimlarni taklif etamiz.", parse_mode="Markdown", reply_markup=get_main_menu())

@dp.message(F.text == "📂 Xizmatlar ko'rsatish")
async def show_services(message: types.Message):
    await message.answer("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())

@dp.message(F.text == "📊 Statistika & Kafolat")
async def show_stats(message: types.Message):
    stats_text = "⚡ **HAXI AGENCY:**\n\n🌐 **5+ Yil** — Tajriba\n👥 **200+** — Mijozlar\n🚀 **200+** — Loyihalar\n🏆 **100%** — Kafolat"
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message(F.text == "📞 Aloqa & Hamkorlik")
async def show_contact(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Suhbat boshlash", url=f"https://t.me/{ADMIN_USERNAME}")]])
    await message.answer(f"✨ Adminga murojaat qiling: @{ADMIN_USERNAME}", reply_markup=kb)

@dp.message(F.text == "🌐 Bizning Sayt (Web App)")
async def show_webapp(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💻 Saytni Ochish", web_app=WebAppInfo(url=NETLIFY_URL))]])
    await message.answer("Premium saytimizni bot ichida ko'ring:", reply_markup=kb)

@dp.callback_query(F.data.startswith("serv_"))
async def process_service_click(callback: types.CallbackQuery):
    service = callback.data.split("_")[1]
    titles = {"bot": ["Telegram Bot", "$140 dan"], "web": ["Veb-Sayt", "$200 dan"], "video": ["AI Video Kliplar", "$100 dan"], "smm": ["Ijtimoiy Tarmoqlar", "$70 dan"]}
    txt = f"🤖 **{titles[service][0]} Xizmati**\n\nPremium va kiber-yechimlar.\n\n💰 **Narxi:** {titles[service][1]}"
    await callback.message.edit_text(txt, parse_mode="Markdown", reply_markup=get_order_keyboard(titles[service][0]))
    await callback.answer()

@dp.callback_query(F.data == "back_to_services")
async def back_services(callback: types.CallbackQuery):
    await callback.message.edit_text("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())
    await callback.answer()

# FEYK PORT WEB SERVER (Render o'chib qolmasligi uchun)
async def handle_index(request):
    return web.Response(text="Bot is live!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
