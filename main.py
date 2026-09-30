import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render Live Server
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_srv():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()

threading.Thread(target=run_srv, daemon=True).start()

# --- আপনার তথ্যগুলো এখানে বসান ---
BOT_TOKEN = "8665209596:AAGU8WrS3DSCYndaYxu3ueMffm7sG-EN-ws"
ADMIN_ID = 2012334358  # আপনার টেলিগ্রাম আইডি নম্বর
TOPFOLLOW_USERNAME = "moinraj2026"
CHANNEL_LINK = "https://t.me/Smart_Earning2"
SUPPORT_USER = "@Moin1239"
# ---------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("💸 Sell Coin 💸"))
    markup.add(types.KeyboardButton("📈 TODAY RATE"), types.KeyboardButton("🔥 Telegram চ্যানেল"))
    markup.add(types.KeyboardButton("📞 SUPPORT"))
    return markup

def cancel_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚫 Cancel"))
    return markup

def payment_methods_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("🧰 বিকাশ (Bkash)"),
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
    text = message.text.strip()
    text_lower = text.lower()

    # ১. Cancel
    if "cancel" in text_lower or "বাতিল" in text or "main menu" in text_lower:
        user_data.pop(chat_id, None)
        bot.send_message(chat_id, "অপারেশন বাতিল করা হয়েছে।", reply_markup=main_menu())
        return

    # ২. Today Rate
    if "rate" in text_lower or "রেট" in text:
        bot.send_message(chat_id, "Top Coin প্রতি 1k Coin = 5.4 Tk ✅")
        return

    # ৩. Channel
    if "চ্যানেল" in text or "channel" in text_lower:
        chan_text = (
            "টেলিগ্রাম চ্যানেলে Join করে ইনকাম করতে থাকুন 👇👇\n\n"
            f"🔥 Link: {CHANNEL_LINK}"
        )
        bot.send_message(chat_id, chan_text)
        return

    # ৪. Support
    if "support" in text_lower or "সাপোর্ট" in text:
        bot.send_message(chat_id, f"যেকোনো প্রয়োজনে যোগাযোগ করুন: {SUPPORT_USER}")
        return

    # ৫. Sell Top Coin (যেভাবেই চাপ দিক সাথে সাথে কাজ করবে)
    if "sell" in text_lower or "কয়েন" in text or "coin" in text_lower:
        user_data[chat_id] = {'step': 'WAIT_COIN'}
        msg_text = (
            "💰 কত হাজার কয়েন বিক্রি করতে চান?\n"
            "সংখ্যায় লিখুন, সর্বনিম্ন 10k Coin, মোট কয়েন লিখুন"
        )
        bot.send_message(chat_id, msg_text, reply_markup=cancel_menu())
        return

    # ৬. কয়েন সংখ্যা নেওয়া
    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_COIN':
        if not text.isdigit() or int(text) < 5000:
            bot.send_message(chat_id, "⚠️ সংখ্যায় লিখুন, সর্বনিম্ন 10k Coin, মোট কয়েন লিখুন:", reply_markup=cancel_menu())
            return
        user_data[chat_id]['amount'] = text
        user_data[chat_id]['step'] = 'WAIT_METHOD'
        bot.send_message(chat_id, "Select Payment Receive Method / পেমেন্ট নেওয়ার মাধ্যম সিলেক্ট করুন:", reply_markup=payment_methods_menu())
        return

    # ৭. বিকাশ বা নগদ সিলেক্ট করা (দুটোই ১০০% কাজ করবে)
    if chat_id in user_data and user_data[chat_id].get('step') == 'WAIT_METHOD':
        if "বিকাশ" in text or "bkash" in text_lower:
            user_data[chat_id]['method'] = "বিকাশ (Bkash)"
            user_data[chat_id]['step'] = 'WAIT_NUMBER'
            bot.send_message(chat_id, "দয়া করে আপনার পার্সোনাল বিকাশ নম্বরটি দিন:", reply_markup=cancel_menu())
            return
        elif "নগদ" in text or "nagad" in text_lower:
            user_data[chat_id]['method'] = "নগদ (Nagad)"
            user_data[chat_id]['step'] = 'WAIT_NUMBER'
            bot.send_message(chat_id, "দয়া করে আপনার পার্সোনাল নগদ নম্বরটি দিন:", reply_markup=cancel_menu())
            return
        else:
            bot.send_message(chat_id, "নিচের বাটন থেকে পেমেন্ট মেথড নির্বাচন করুন:", reply_markup=payment_methods_menu())
            return

    # ৮. নম্বর নেওয়া
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
