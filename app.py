from flask import Flask, request, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

app = Flask(__name__)

# Прямо указываем токен вашего бота
BOT_TOKEN = '6630264932:AAFf9zYIgAlSTAp4AzCgikGKKXgWg44mIes'

# Инициализация Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Хэндлеры для бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Лайт Режим", callback_data='lite')],
        [InlineKeyboardButton("Рейдж Режим", callback_data='rage')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите режим:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mode = query.data
    coefficient = calculate_coefficient(mode)
    await query.edit_message_text(text=f"Режим: {mode.capitalize()} - Коэффициент: {coefficient}")

def calculate_coefficient(mode):
    import random
    if mode == 'lite':
        return round(random.uniform(1.01, 2.2), 2)
    elif mode == 'rage':
        return round(random.uniform(1.7, 7), 2)

# Роут для вебхука Telegram
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.update_queue.put(update)  # Добавили await здесь
    return 'ok'

# Основной рендеринг HTML страницы
@app.route('/')
def index():
    return render_template('predict.html')

# Запуск Flask приложения
def main():
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(CallbackQueryHandler(button))

    # Используем значение порта из окружения
    port = int(os.getenv("PORT", 8080))  # Включает дефолтное значение для проверки
    print(f"Application is running on port: {port}")  # Временный вывод для отладки
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
