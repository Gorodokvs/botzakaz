import re
import telebot  # Импорт библиотеки для работы с Telegram API
import sqlite3  # Импорт библиотеки для работы с базой данных SQLite
import requests  # Импорт библиотеки для отправки HTTP-запросов
from telebot import types  # Импорт типов для работы с клавиатурами
deliveryMethod = ''
paymentMethod = ''
salda_chat_id = 380781080
sibtrakt_chat_id = 424347833
kachkanar_chat_id = 6209470364
allowed_users = [380781080, 424347833]
# Создаем экземпляр бота с указанием токена
bot = telebot.TeleBot('7647629268:AAE2HacxBvRl3etkfcIT8gzMz6XSZ3WXsVU')



@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in allowed_users:
        conn = sqlite3.connect("zakaz2")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                OrderNumber TEXT,
                CreationDate TEXT,
                OrderAmount INTEGER,
                DeliveryMethod TEXT,
                PaymentMethod TEXT,
                Recipient TEXT,
                RecipientPhone TEXT,
                Region TEXT,
                City TEXT,
                DeliveryAddress TEXT,
                Comment TEXT,
                Products TEXT
            );
        ''')
        conn.commit()  # Подтверждаем изменения в базе данных
        bot.reply_to(message, "Готов")  # Ответ пользователю
        print(message.chat.id)  # Вывод идентификатора чата
        conn.close()  # Закрываем соединение с базой данных
    else:
        bot.reply_to(message, "У вас нет доступа к этой команде. 🚫")

@bot.message_handler(commands=['info'])
def info(message):
    conn = sqlite3.connect("zakaz2")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Выбор всех записей из таблицы users
    for row in cursor.fetchall():  # Вывод всех записей в консоль
        print(row)
    conn.close()  # Закрываем соединение с базой данных


# Обработчик для получения информации от пользователя
@bot.message_handler(func=lambda message: message.from_user.id in allowed_users)
def handle_order(message):
    global deliveryMethod
    global paymentMethod
    orders = message.text.split(',')


    # Проверка на наличие всех необходимых данных
    if len(orders) >= 12:
        conn = sqlite3.connect("zakaz2")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (OrderNumber, CreationDate, OrderAmount, DeliveryMethod, PaymentMethod, Recipient, RecipientPhone, Region, City, DeliveryAddress, Comment, Products) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)
        ''', (
            orders[0],  # OrderNumber
            orders[1],  # CreationDate
            orders[2],  # OrderAmount
            orders[3],  # DeliveryMethod
            orders[4],  # PaymentMethod
            orders[5],  # Recipient
            orders[6],  # RecipientPhone
            orders[7],  # Region
            orders[8],  # City
            orders[9],  # DeliveryAddress
            orders[10],  # Comment
            orders[11]  # Products
        ))
        conn.commit()  # Подтверждаем изменения в базе данных
        conn.close()  # Закрываем соединение с базой данных

        if int(orders[3]) == 1:
            deliveryMethod = 'Самовывоз'
        elif int(orders[3]) == 2:
            deliveryMethod = 'Доставка курьером'
        if int(orders[4]) == 3:
            paymentMethod = 'Наличные'
        elif int(orders[4]) == 4:
            paymentMethod = 'Банковской картой'
        elif int(orders[4]) == 5:
            paymentMethod = 'Оплата через сайт'
        # Формирование сообщения без названий полей
        formatted_message = (
            f"Номер заказа: {orders[0]}\n"
            f"Дата: {orders[1]}\n"
            f"Сумма заказа: {orders[2]}\n"
            f"Метод доставки: {deliveryMethod}\n"
            f"Метод оплаты: {paymentMethod}\n"
            f"Имя: {orders[5]}\n"
            f"Телефон: {orders[6]}\n"
            f"Город: {orders[8]}\n"
            f"Адрес доставки: {orders[9]}\n"
            f"Заказ:\n{orders[11]}\n"
            f"Комментарий: {orders[10]}\n"
        )

        otvet = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("20минут", callback_data='20')
        button2 = types.InlineKeyboardButton("30минут", callback_data='30')
        button3 = types.InlineKeyboardButton("60минут", callback_data='60')
        button4 = types.InlineKeyboardButton("90минут", callback_data='90')
        otvet.add(button1, button2, button3, button4)

        # Отправка сообщения с форматированным текстом
        if  int(orders[7]) == 109:
            bot.send_message(salda_chat_id, formatted_message, reply_markup=otvet)

        elif int(orders[7]) == 110:
            bot.send_message(sibtrakt_chat_id, formatted_message, reply_markup=otvet)
        elif int(orders[7]) == 112:
            bot.send_message(kachkanar_chat_id, formatted_message, reply_markup=otvet)
    else:
        # Если данных недостаточно, отправляем простое сообщение
        bot.send_message(380781080, message.text)  # Отправка сообщения в указанный чат


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == "20":
            print()
            bot.send_message(call.message.chat.id, "Круто!")  # Ответ на нажатие первой кнопки
        elif call.data == "30":
            bot.send_message(call.message.chat.id, "все еще не плохо")  # Ответ на нажатие второй кнопки
        elif call.data == "60":
            bot.send_message(call.message.chat.id, "можно и побыстрее")  # Ответ на нажатие третьей кнопки
        elif call.data == "90":
            bot.send_message(call.message.chat.id, "очень долго")  # Ответ на нажатие четвертой кнопки

        bot.send_message(call.message.chat.id, f"Ваш выбор: {call.data}\nОтвет: {call.message.text}")

        start_index = call.message.text.find("Телефон:")
        if start_index != -1:
            # Извлекаем текст с "Телефон:" до конца строки
            phone_info = call.message.text[start_index:][12:26]
            phone_info = phone_info.replace("(", "").replace(")", "").replace("+", "").replace("-", "").strip()
        else:
            phone_info = "Телефон не найден."


        messSMS = "Ваш заказ готов через "+call.data+" минут"

        r = requests.get('http://192.168.1.102/default/en_US/send.html?u=admin&p=admin&l=2&n=8'+phone_info+'&m='+messSMS)
        print(phone_info)
        print(messSMS)
        print(r)
        # Удаление клавиатуры после нажатия
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)

    except Exception as e:  # Обработка исключений
        print(repr(e))  # Вывод ошибки в консоль


# Запуск бота в бесконечном цикле
bot.polling(none_stop=True)