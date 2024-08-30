import os
from flask import Flask, request
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided")

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
