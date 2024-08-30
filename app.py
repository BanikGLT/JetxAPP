import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка Flask приложения
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка наличия токена
if not BOT_TOKEN:
    logger.error("Не указан токен бота!")
    raise RuntimeError("Необходимо указать токен бота через переменную окружения BOT_TOKEN")

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    await update.message.reply_text("Бот запущен!")

# Добавляем обработчик команды /start в приложение Telegram
telegram_app.add_handler(CommandHandler("start", start))

# Роут для обработки вебхуков
@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return "ok"
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return "error", 500

# Запуск Flask сервера
port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
