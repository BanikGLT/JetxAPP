from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import requests

app = Flask(__name__)

# Токен вашего бота
BOT_TOKEN = '7281342493:AAF6zV24Mhktx1OCeZHnozwbBkOsrKN0Ztk'

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Получаем URL вебхука из переменной окружения, настроенной в Railway
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Эта переменная окружения будет установлена в Railway

def set_webhook():
    """
    Устанавливаем вебхук для Telegram бота при запуске приложения.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/webhook"}
    response = requests.post(url, data=data)
    print("Webhook set:", response.json())

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /start и предлагает выбор режима.
    """
    keyboard = [
        [InlineKeyboardButton("Лайт Режим", callback_data='lite')],
        [InlineKeyboardButton("Рейдж Режим", callback_data='rage')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите режим:', reply_markup=reply_markup)

# Хэндлер для обработки нажатий кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает нажатия кнопок с выбором режима и выводит рассчитанный коэффициент.
    """
    query = update.callback_query
    await query.answer()
    mode = query.data
    coefficient = calculate_coefficient(mode)
    await query.edit_message_text(text=f"Режим: {mode.capitalize()} - Коэффициент: {coefficient}")

# Функция для вычисления коэффициента на основе выбранного режима
def calculate_coefficient(mode):
    """
    Вычисляет коэффициент в зависимости от выбранного режима.
    """
    import random
    if mode == 'lite':
        return round(random.uniform(1.01, 2.2), 2)
    elif mode == 'rage':
        return round(random.uniform(1.7, 7), 2)

# Роут для обработки запросов вебхука Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Получает обновления от Telegram через вебхук и передает их в обработку боту.
    """
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)  # Обработка обновления
    return 'ok'

# Роут для отображения основного HTML интерфейса
@app.route('/')
def index():
    """
    Возвращает HTML страницу с интерфейсом для выбора режима.
    """
    return render_template('predict.html')

# Главная функция запуска приложения
def main():
    """
    Устанавливает вебхук и запускает сервер через Waitress.
    """
    set_webhook()  # Устанавливаем вебхук при запуске приложения
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(CallbackQueryHandler(button))
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
