import os
from threading import Thread
from flask import Flask
import telebot

# --- إعداد خادم Flask لإبقاء البوت نشطاً على Railway ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

keep_alive()

# --- الاتصال بـ Telegram عبر التوكن ---
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- فحص وتصفية الحسابات الوهمية (عند كتابة /start) ---
@bot.message_handler(commands=['start'])
def verify_user(message):
    user = message.from_user

    # 1. فحص وجود اسم مستخدم (Username)
    if not user.username:
        bot.reply_to(message, "⚠️ عذراً، لا يمكن استخدام البوت من قبل حسابات وهمية (يجب تعيين اسم مستخدم Username في حسابك أولاً).")
        return

    # 2. فحص وجود صورة شخصية (Profile Photo)
    try:
        user_photos = bot.get_user_profile_photos(user.id)
        if user_photos.total_count == 0:
            bot.reply_to(message, "⚠️ عذراً، يجب وضع صورة شخصية لحسابك لاستخدام البوت.")
            return
    except Exception:
        pass

    # إذا اجتاز الحساب الفحوصات بنجاح
    bot.reply_to(message, f"أهلاً بك يا {user.first_name}! ✅ تم التحقق من حسابك بنجاح، البوت يعمل الآن وجاهز للاستخدام.")

# --- الاستجابة لباقي الرسائل النصية ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"وصلت رسالتك: {message.text}")

# --- تشغيل البوت باستمرار ---
if __name__ == "__main__":
    bot.infinity_polling()
import os
from threading import Thread
from flask import Flask
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

keep_alive()

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل الآن على الاستضافة 24/7.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"وصلت رسالتك: {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()
