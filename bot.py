import telebot
from telebot import types

#Сюда свой токен полученный от @BotFather
TOKEN = 'ТВОЙ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Товары (в реальном боте берутся из БД)
PRODUCTS = {
    'prod_1': {'name': 'Курс по Python', 'price': 1000, 'desc': 'Базовый курс для новичков.'},
    'prod_2': {'name': 'Курс по C#', 'price': 1200, 'desc': 'Продвинутый курс по C#.'},
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🛒 Каталог', callback_data='catalog')
    btn2 = types.InlineKeyboardButton('📞 Контакты', callback_data='contacts')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "Добро пожаловать в демо-магазин! Выберите действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'catalog':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for prod_id, prod_info in PRODUCTS.items():
            btn = types.InlineKeyboardButton(f"{prod_info['name']} - {prod_info['price']}₽", callback_data=f"view_{prod_id}")
            markup.add(btn)
        btn_back = types.InlineKeyboardButton('⬅️ Назад', callback_data='back')
        markup.add(btn_back)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="📋 Каталог товаров:", reply_markup=markup)

    elif call.data.startswith('view_'):
        prod_id = call.data.split('_')[1]
        prod = PRODUCTS[prod_id]
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_buy = types.InlineKeyboardButton('💳 Купить', callback_data=f"buy_{prod_id}")
        btn_back = types.InlineKeyboardButton('⬅️ Назад в каталог', callback_data='catalog')
        markup.add(btn_buy, btn_back)
        
        text = f"*{prod['name']}*\n\n{prod['desc']}\n\nЦена: {prod['price']}₽"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=text, reply_markup=markup, parse_mode='Markdown')

    elif call.data.startswith('buy_'):
        prod_id = call.data.split('_')[1]
        bot.answer_callback_query(call.id, text="Спасибо за заказ! (Демо)")
        bot.send_message(call.message.chat.id, f"Вы заказали: {PRODUCTS[prod_id]['name']}. Оформление заказа в демо-режиме.")

    elif call.data == 'contacts':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="📞 Наши контакты:\nТелефон: +7 (999) 123-45-67\nEmail: demo@shop.com", 
                              reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back')))
    
    elif call.data == 'back':
        # Возврат в главное меню
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🛒 Каталог', callback_data='catalog')
        btn2 = types.InlineKeyboardButton('📞 Контакты', callback_data='contacts')
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="Выберите действие:", reply_markup=markup)

if __name__ == '__main__':
    print("Магазин запущен...")
    bot.polling(none_stop=True)
