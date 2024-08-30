import os
from quart import Quart, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Необходимо указать токен бота через переменную окружения BOT_TOKEN")

# Инициализируем приложение Quart
app = Quart(__name__)

# Создаем приложение Telegram с токеном
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Это стартовое сообщение.")

telegram_app.add_handler(CommandHandler("start", start))

# Вебхук для обработки запросов от Telegram
@app.route('/webhook', methods=['POST'])
async def webhook():
    json_data = await request.get_json()
    update = Update.de_json(json_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Запуск Quart приложения
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
