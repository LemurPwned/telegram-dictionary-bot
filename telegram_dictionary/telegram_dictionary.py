import logging
import os
from ast import parse
from queue import Queue

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .wiktionary import WikiRequest, escape_markdown

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

builder = Application.builder()
builder.token(os.environ['TOKEN']).build()
application = builder.build()

q = Queue()

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mkd_start = """
    *Welcome to the Telegram Dictionary* \n
    This bot is a simple dictionary that uses `Wiktionary` as a source.
    To ask for a definition, type in:\n `ask <word>`.
    """
    mkd_start = escape_markdown(mkd_start)
    await context.bot.send_message(chat_id=update.effective_chat.id,
    text=mkd_start, parse_mode='MarkdownV2')


async def word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_says = " ".join(context.args)
    if not user_says:
        await update.message.reply_text(escape_markdown(r"Please type a request as: `/ask <word>`"),
        parse_mode='MarkdownV2')
        return
    await update.message.reply_text("You asked for a definition: " + user_says)
    try:
        word = WikiRequest(user_says)
    except ValueError:
        await update.message.reply_text("No sensible word found in Wiktionary")
        return
    logging.debug("Word request: " + str(word.word))
    q.put(word, block=False)
    await update.message.reply_text(str(word), parse_mode='MarkdownV2')

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
