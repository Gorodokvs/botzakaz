import telebot
import  sqlite3
import requests
from telebot import  types
# crfxfnm

#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[





bot = telebot.TeleBot('7647629268:AAE2HacxBvRl3etkfcIT8gzMz6XSZ3WXsVU')

@bot.message_handler(commands=['sendsms'])
def sendsms(message):
    r = requests.get('http://192.168.1.102/default/en_US/send.html?u=admin&p=admin&l=2&n=89995655668&m=test')
    print('ok')


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect("zakaz2")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            OrderNumber TEXT,
            CreationDate TEXT,
            OrderAmount REAL,
            DeliveryMethod TEXT,
            PaymentMethod TEXT,
            Recipient TEXT,
            RecipientPhone TEXT,
            Region TEXT,
            City TEXT,
            DeliveryAddress TEXT,
            Comment TEXT
        );
    ''')
    conn.commit()
    bot.reply_to(message, "Готов")
    print(message.chat.id)
    conn.close()

@bot.message_handler(commands=['info'])
def info(message):
    conn = sqlite3.connect("zakaz2")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)
    conn.close()



@bot.message_handler(func=lambda message: True)
def info(message):
    orders = message.text
    conn = sqlite3.connect("zakaz2")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (OrderNumber, CreationDate, OrderAmount, DeliveryMethod, PaymentMethod, Recipient, RecipientPhone, Region, City, DeliveryAddress, Comment) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        orders.split(',')[0],  # OrderNumber
        orders.split(',')[1],  # CreationDate
        orders.split(',')[2],  # OrderAmount
        orders.split(',')[3],  # DeliveryMethod
        orders.split(',')[4],  # PaymentMethod
        orders.split(',')[5],  # Recipient
        orders.split(',')[6],  # RecipientPhone
        orders.split(',')[7],  # Region
        orders.split(',')[8],  # City
        orders.split(',')[9],  # DeliveryAddress
        orders.split(',')[10]  # Comment
    ))
    conn.commit()
    conn.close()


    otvet = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("20минут", callback_data='20')
    button2 = types.InlineKeyboardButton("30минут", callback_data='30')
    button3 = types.InlineKeyboardButton("60минут", callback_data='60')
    button4 = types.InlineKeyboardButton("90минут", callback_data='90')
    otvet.add(button1, button2, button3, button4)
    bot.send_message(380781080, message.text, reply_markup=otvet)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == "20":
            bot.send_message(call.message.chat.id, "Круто!")
        elif call.data == "30":
            bot.send_message(call.message.chat.id, "все еще не плохо")
        elif call.data == "60":
            bot.send_message(call.message.chat.id, "можно и побыстрее")
        elif call.data == "90":
            bot.send_message(call.message.chat.id, "очень долго")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    except Exception as e:
        print(repr(e))






bot.polling(none_stop=True)