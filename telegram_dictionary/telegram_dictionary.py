import logging
import os
from queue import Queue

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .wiktionary import WikiRequest

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

builder = Application.builder()
builder.token(os.environ['TOKEN']).build()
application = builder.build()

q = Queue()

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
    text="I'm a bot, please talk to me!")


async def word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_says = " ".join(context.args)
    await update.message.reply_text("You asked for a definition: " + user_says)
    word = WikiRequest(user_says)
    logging.debug("Word request: " + str(word.word))
    q.put(word, block=False)
    await update.message.reply_text(str(word))

async def save_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug("Saving")
    try:
        last_word_message = q.get()
        await update.message.reply_text("Saving a word: " + last_word_message.word)
    except:
        await update.message.reply_text("No word to save")

application.add_handler(CommandHandler("start", start_callback))
application.add_handler(CommandHandler("ask", word_callback))
application.add_handler(CommandHandler("save", save_callback))
