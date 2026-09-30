import telebot
from telebot import types

# --- আপনার তথ্যগুলো এখানে কোটেশনের ভেতরে বসান ---
BOT_TOKEN = "8665209596:AAGU8WrS3DSCYndaYxu3ueMffm7sG-EN-ws"
ADMIN_ID = 2012334358  # এখানে আপনার সেই টেলিগ্রাম ID নম্বরটি দিন (কোনো কোটেশন ছাড়া)
TOPFOLLOW_USERNAME = "moinraj2026"
CHANNEL_LINK = "https://t.me/Smart_Earning2"
SUPPORT_USER = "@Moin1239"  # আপনার টেলিগ্রাম ইউজারনেম
# -----------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# মূল মেনু
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_sell = types.KeyboardButton("🥇 Coin Sell 🥇")
    btn_rate = types.KeyboardButton("📈 TODAY RATE")
    btn_chan = types.KeyboardButton("🔥 Telegram চ্যানেল")
    btn_sup = types.KeyboardButton("📞 SUPPORT")
    markup.add(btn_sell)
    markup.add(btn_rate, btn_chan)
    markup.add(btn_sup)
    return markup

# ক্যান্সেল বাটন
def cancel_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚫 Cancel"))
    return markup

# পেমেন্ট মেথড বাটন
def payment_methods_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("💼 বিকাশ (BKash)"),
        types.KeyboardButton("💼 নগদ (Nagad)"),
        types.KeyboardButton("🚫 Cancel")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_data.pop(message.chat.id, None)
    text = (
        "🚀 শুরু করতে নিচের মেনু থেকে একটি অপশন নির্বাচন করুন।\n\n"
        "⚠️ লেনদেনের আগে সব তথ্য ভালোভাবে যাচাই করুন।"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.message_handler(func=lambda msg: True, content_types=['text'])
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    if text == "🚫 Cancel" or text == "Main Menu":
        user_data.pop(chat_id, None)
        bot.send_message(chat_id, "অপারেশন বাতিল করা হয়েছে।", reply_markup=main_menu())
        return

    if text == "📈 TODAY RATE":
        bot.send_message(chat_id, "New Top Coin প্রতি 1k Coin = 5.5 Tk ✅")
        return

    if text == "🔥 Telegram চ্যানেল":
        chan_text = (
            "টেলিগ্রাম চ্যানেলে Join করে ইনকাম করতে থাকুন 👇👇\n\n"
            f"🔥 Link: {CHANNEL_LINK}"
        )
        bot.send_message(chat_id, chan_text)
        return

    if text == "📞 SUPPORT":
        bot.send_message(chat_id, f"যেকোনো প্রয়োজনে যোগাযোগ করুন: {SUPPORT_USER}")
        return

    if text == "🥇 Coin Sell 🥇":
        user_data[chat_id] = {'step': 'WAIT_COIN'}
        msg_text = (
            "💰 কত হাজার কয়েন বিক্রি করতে চান?\n"
            "সংখ্যায় লিখুন, সর্ব নিম্ন ( 10,000 )  কয়েন লিখুন"
        )
        bot.send_message(chat_id, msg_text, reply_markup=cancel_menu())
        return

    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_COIN':
        if not text.isdigit() or int(text) < 5000:
            bot.send_message(chat_id, "⚠️ সংখ্যায় লিখুন, সর্ব নিম্ন ( 10,000 ) কয়েন লিখুন:", reply_markup=cancel_menu())
            return
        
        user_data[chat_id]['amount'] = text
        user_data[chat_id]['step'] = 'WAIT_METHOD'
        bot.send_message(chat_id, "Select Payment Receive Method / পেমেন্ট নেওয়ার মাধ্যম সিলেক্ট করুন:", reply_markup=payment_methods_menu())
        return

    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_METHOD':
        if text in ["🧰 বিকাশ (bKash)", "💼 নগদ (Nagad)"]:
            user_data[chat_id]['method'] = text
            user_data[chat_id]['step'] = 'WAIT_NUMBER'
            bot.send_message(chat_id, f"দয়া করে আপনার পার্সোনাল {text} নম্বরটি দিন:", reply_markup=cancel_menu())
        return

    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_NUMBER':
        user_data[chat_id]['number'] = text
        user_data[chat_id]['step'] = 'WAIT_PHOTO'
        
        caption_text = (
            "[🗒]\n"
            "📸 এই ইউজারনেমে Top Coin পাঠিয়ে একটি স্ক্রিনশট আপলোড করুন।\n\n"
            f"ইউজারনেম 👉 \n`{TOPFOLLOW_USERNAME}`\n 👈\n\n"
            "🛡️ Screenshot জমা দিন"
        )
        bot.send_message(chat_id, caption_text, parse_mode="Markdown", reply_markup=cancel_menu())
        return

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_PHOTO':
        photo_id = message.photo[-1].file_id
        amount = user_data[chat_id].get('amount')
        method = user_data[chat_id].get('method')
        number = user_data[chat_id].get('number')
        username = f"@{message.from_user.username}" if message.from_user.username else "ইউজারনেম নেই"

        admin_report = (
            f"🔔 **নতুন কয়েন বিক্রির রিকোয়েস্ট এসেছে!**\n\n"
            f"👤 কাস্টমার: {message.from_user.first_name} ({username})\n"
            f"🆔 Telegram ID: `{chat_id}`\n"
            f"🪙 কয়েন পরিমাণ: {amount}\n"
            f"💳 মেথড: {method}\n"
            f"📞 পেমেন্ট নম্বর: `{number}`"
        )
        bot.send_photo(ADMIN_ID, photo_id, caption=admin_report, parse_mode="Markdown")

        bot.send_message(chat_id, "✅ আপনার স্ক্রিনশট ও তথ্য সফলভাবে জমা হয়েছে!\nঅ্যাডমিন ভেরিফাই করে কিছুক্ষণের মধ্যে টাকা পাঠিয়ে দেবে। ধন্যবাদ!", reply_markup=main_menu())
        user_data.pop(chat_id, None)

bot.infinity_polling()
