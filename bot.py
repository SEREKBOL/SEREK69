import telebot
import requests
from telebot import types

# --- ТОХИРГОО ---
BOT_TOKEN = "8719142642:AAF9KoXEBF-MDV1po3jr0_EgltBn_IBJ6MI"
FIREBASE_URL = "https://telmunn-79711-default-rtdb.firebaseio.com/users.json"
GITHUB_LINK = "https://github.com/SEREKBOL/SEREK69.git"
CHANNEL_ID = "@TarganJack_channel"
CHANNEL_LINK = "https://t.me/TarganJack_channel"

bot = telebot.TeleBot(BOT_TOKEN)

# 1. Сувагт элссэн эсэхийг шалгах
def is_joined(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# 2. Firebase-ээс дата унших
def get_user_data(chat_id):
    try:
        db = requests.get(FIREBASE_URL, timeout=10).json()
        if db:
            for key in db:
                if str(db[key].get('telegram_id')) == str(chat_id):
                    return db[key]
        return None
    except: return None

# 3. Товчлуурууд
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('TERMUX'), types.KeyboardButton('IOS'))
    markup.add(types.KeyboardButton('💼 Balance'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if not is_joined(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Сувагт элсэх", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, "❗ Та эхлээд манай сувагт элсэх ёстой!", reply_markup=markup)
        return

    user_data = get_user_data(message.chat.id)
    key = user_data.get('key', 'Not Found') if user_data else 'Not Found'
    bal = user_data.get('balance', 0) if user_data else 0
    
    welcome = (
        "‍┌ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ 𝗞𝗮𝘆𝘇𝗲𝗻𝘀ʜ𝗼ᴘ!\n"
        "└We're excited to have you on board\n\n"
        "ʜᴇʀᴇ ᴀʀᴇ ꜱᴏᴍᴇ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴅᴇᴛᴀɪʟꜱ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ:\n\n"
        f"┌🆔 ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ: `{message.chat.id}`\n"
        f"├🔑 ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ: `{key}`\n"
        f"└💰 ʙᴀʟᴀɴᴄᴇ: `{bal:,}`\n\n"
        "┌💫 ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴛʜᴇ ꜰᴇᴀᴛᴜʀᴇꜱ ᴡᴇ ᴏꜰꜰᴇʀ\n"
        "├💬 ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ ᴏʀ ɴᴇᴇᴅ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ, ᴊᴜꜱᴛ\n"
        "│ʟᴇᴛ ᴜꜱ ᴋɴᴏᴡ\n"
        "└🚀 ᴇɴᴊᴏʏ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ!!"
    )
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '💼 Balance' or m.text == '/balance')
def bal_cmd(message):
    if not is_joined(message.from_user.id): return
    user_data = get_user_data(message.chat.id)
    if user_data:
        blocked = "Yes ☠️" if user_data.get('is_blocked') else "No 🚫"
        msg = (
            "💼 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 ‍\n\n"
            f"🆔 ┌ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ: `{message.chat.id}`\n"
            f"💰 ├ʙᴀʟᴀɴᴄᴇ: `{user_data.get('balance'):,}`\n"
            f"🚫 └ʙʟᴏᴄᴋᴇᴅ: {blocked}"
        )
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Бүртгэл олдсонгүй.")

@bot.message_handler(func=lambda m: m.text in ['TERMUX', 'IOS'])
def send_code(message):
    if not is_joined(message.from_user.id): return
    if message.text == 'TERMUX':
        code = f"apt update && apt upgrade -y && pkg install python git -y && pip install requests rich pystyle && git clone {GITHUB_LINK} && cd SEREK69 && python tool.py"
        bot.send_message(message.chat.id, f"🚀 **TERMUX CODE:**\n\n`{code}`", parse_mode="Markdown")
    else:
        code = f"apk update && apk add python3 py3-pip git && pip install requests rich pystyle && git clone {GITHUB_LINK} && cd SEREK69 && python3 tool.py"
        bot.send_message(message.chat.id, f"🍎 **IOS iSH CODE:**\n\n`{code}`", parse_mode="Markdown")

bot.infinity_polling()

