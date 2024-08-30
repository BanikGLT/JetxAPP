from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Используем переменную окружения для токена бота
BOT_TOKEN = os.getenv('6630264932:AAFf9zYIgAlSTAp4AzCgikGKKXgWg44mIes')  # Убедитесь, что переменная окружения установлена

# Инициализация Telegram Bot
try:
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Проверка успешного подключения
    bot_info = telegram_app.bot.get_me()
    logger.info(f"Bot successfully connected: {bot_info.username}")
except Exception as e:
    logger.error(f"Failed to connect bot: {e}")
    raise

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Зайти в приложение", url="https://banikglt-jetxapp-d85a.twc1.net")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажмите на кнопку ниже, чтобы зайти в приложение:', reply_markup=reply_markup)

# Роут для Telegram вебхука
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return 'ok'

# Главная функция запуска приложения
def main():
    telegram_app.add_handler(CommandHandler('start', start))

    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

if __name__ == '__main__':
    main()
