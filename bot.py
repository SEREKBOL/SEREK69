import telebot
import requests

# --- ТОХИРГОО ---
BOT_TOKEN = "8719142642:AAF9KoXEBF-MDV1po3jr0_EgltBn_IBJ6MI"
FIREBASE_URL = "https://telmunn-79711-default-rtdb.firebaseio.com/users.json"
GITHUB_LINK = "https://github.com/SEREKBOL/SEREK69.git"

bot = telebot.TeleBot(BOT_TOKEN)

# Firebase-ээс дата хайх функц
def get_user_data(chat_id):
    try:
        response = requests.get(FIREBASE_URL, timeout=10)
        db = response.json()
        if db:
            for uid, data in db.items():
                if str(data.get('telegram_id')) == str(chat_id):
                    return data
        return None
    except:
        return None

# 1. /start КАНД
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_data = get_user_data(message.chat.id)
    access_key = user_data.get('key', 'Not Found') if user_data else 'Not Found'
    balance = user_data.get('balance', 0) if user_data else 0
    
    msg = (
        "‍┌ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ 𝗞𝗮𝘆𝘇𝗲𝗻𝘀ʜ𝗼ᴘ!\n"
        "└We're excited to have you on board\n\n"
        "ʜᴇʀᴇ ᴀʀᴇ ꜱᴏᴍᴇ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴅᴇᴛᴀɪʟꜱ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ:\n\n"
        f"┌🆔 ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ: {message.chat.id}\n"
        f"├🔑 ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ: {access_key}\n"
        f"└💰 ʙᴀʟᴀɴᴄᴇ: {balance:,}\n\n"
        "┌💫 ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴛʜᴇ ꜰᴇᴀᴛᴜʀᴇꜱ ᴡᴇ ᴏꜰꜰᴇʀ\n"
        "├💬 ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ ᴏʀ ɴᴇᴇᴅ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ, ᴊᴜꜱᴛ\n"
        "│ʟᴇᴛ ᴜꜱ ᴋɴᴏᴡ\n"
        "└🚀 ᴇɴᴊᴏʏ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ!!"
    )
    bot.send_message(message.chat.id, msg)

# 2. "balance" ТЕКСТ ШАЛГАХ
@bot.message_handler(func=lambda m: m.text and m.text.lower() == 'balance')
def balance_text(message):
    user_data = get_user_data(message.chat.id)
    if user_data:
        bal = user_data.get('balance', 0)
        is_blocked = "Yes 🚫" if user_data.get('is_blocked') else "No ✅"
        msg = (
            "💼 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 ‍\n\n"
            f"🆔 ┌ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ: {message.chat.id}\n"
            f"💰 ├ʙᴀʟᴀɴᴄᴇ: {bal:,}\n"
            f"🚫 └ʙʟᴏᴄᴋᴇᴅ: {is_blocked}"
        )
    else:
        msg = "❌ Таны бүртгэл олдсонгүй."
    bot.send_message(message.chat.id, msg)

# 3. "CODE" ГЭЖ БИЧИХЭД ХАРИУЛАХ
@bot.message_handler(func=lambda m: m.text and m.text.upper() == 'CODE')
def code_text(message):
    bot.send_message(message.chat.id, "Ene code ghdee menu bish shvv\n\n👉 **TERMUX**\n👉 **IOS**\n\nГэж бичнэ үү.")

# 4. "TERMUX" БОЛОН "IOS" ГЭЖ БИЧИХЭД КОД ӨГӨХ
@bot.message_handler(func=lambda m: m.text)
def handle_all_text(message):
    txt = message.text.upper()
    
    if txt == "TERMUX":
        # Android Termux code
        code = f"apt update && apt upgrade -y && pkg install python git -y && pip install requests rich pystyle && git clone {GITHUB_LINK} && cd SEREK69 && python tool.py"
        bot.send_message(message.chat.id, f"🚀 **TERMUX:**\n\n`{code}`", parse_mode="Markdown")
        
    elif txt == "IOS":
        # iOS iSH shell code
        code = f"apk update && apk add python3 py3-pip git && pip install requests rich pystyle && git clone {GITHUB_LINK} && cd SEREK69 && python3 tool.py"
        bot.send_message(message.chat.id, f"🍎 **IOS:**\n\n`{code}`", parse_mode="Markdown")
    
    elif txt == "START":
        start_cmd(message)

print("Бот ажиллаж байна (Зөвхөн текстэн хариулт)...")
bot.infinity_polling()

