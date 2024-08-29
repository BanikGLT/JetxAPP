from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import requests

app = Flask(__name__)

# Используем токен вашего бота
BOT_TOKEN = '7281342493:AAF6zV24Mhktx1OCeZHnozwbBkOsrKN0Ztk'

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Установка вебхука автоматически при запуске
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Получаем URL вебхука из переменной окружения

def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/webhook"}
    response = requests.post(url, data=data)
    print("Webhook set:", response.json())

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Лайт Режим", callback_data='lite')],
        [InlineKeyboardButton("Рейдж Режим", callback_data='rage')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите режим:', reply_markup=reply_markup)

# Хэндлер для обработки нажатий кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mode = query.data
    coefficient = calculate_coefficient(mode)
    await query.edit_message_text(text=f"Режим: {mode.capitalize()} - Коэффициент: {coefficient}")

# Функция для вычисления коэффициента
def calculate_coefficient(mode):
    import random
    if mode == 'lite':
        return round(random.uniform(1.01, 2.2), 2)
    elif mode == 'rage':
        return round(random.uniform(1.7, 7), 2)

# Роут для Telegram вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)  # Обработка обновления
    return 'ok'

# Роут для основного HTML интерфейса
@app.route('/')
def index():
    return render_template('predict.html')

# Функция для запуска приложения
def main():
    set_webhook()  # Устанавливаем вебхук при запуске
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(CallbackQueryHandler(button))
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
