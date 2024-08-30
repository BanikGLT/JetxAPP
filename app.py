from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

app = Flask(__name__)

# Прямо указываем токен вашего бота
BOT_TOKEN = '6630264932:AAFf9zYIgAlSTAp4AzCgikGKKXgWg44mIes'

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    website_url = "https://banikglt-jetxapp-d85a.twc1.net"  # URL вашего сайта
    keyboard = [
        [InlineKeyboardButton("Зайти в приложение", url=website_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Нажмите кнопку ниже, чтобы зайти в приложение.', reply_markup=reply_markup)

# Роут для Telegram вебхука
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return 'ok'

# Роут для отображения основного HTML интерфейса
@app.route('/')
def index():
    return render_template('predict.html')

# Главная функция запуска приложения
def main():
    telegram_app.add_handler(CommandHandler('start', start))

    # Запуск Flask приложения
    port = int(os.getenv("PORT", 8080))  # Порт будет установлен Timeweb Cloud
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
