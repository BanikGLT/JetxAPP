from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

app = Flask(__name__)

# Токен вашего бота
BOT_TOKEN = '6630264932:AAFf9zYIgAlSTAp4AzCgikGKKXgWg44mIes'

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Инициализация приложения
async def initialize_app():
    await telegram_app.initialize()

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    website_url = "https://banikglt-jetxapp-7017.twc1"
    keyboard = [
        [InlineKeyboardButton("Зайти в приложение", url=website_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Нажмите кнопку ниже, чтобы зайти в приложение.', reply_markup=reply_markup)

# Роут для Telegram вебхука
@app.route('/webhook', methods=['POST'])
async def webhook():
    await initialize_app()  # Инициализация приложения
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return 'ok'

# Роут для отображения основного HTML интерфейса
@app.route('/')
def index():
    return render_template('predict.html')

# Добавляем новый маршрут для Bombucks.html
@app.route('/bombucks')
def bombucks():
    return render_template('Bombucks.html')

# Главная функция запуска приложения
def main():
    telegram_app.add_handler(CommandHandler('start', start))

    # Запуск Flask приложения
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
