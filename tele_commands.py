import requests
import random
import time
import os
from dotenv import load_dotenv
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import filters

load_dotenv()

JREMPIRE_ID = os.getenv('JREMPIRE_ID')
WEIKANGBOT_ID = os.getenv('WEIKANGBOT_ID')

messages = [
    'Haii',
    'How is Rui and Ruth?',
    'How is Gwen?',
    'How is Ervin?',
    'May we gather our focus?',
    'If Ervin has no supporters, then that means I am no longer on earth. If the world is against Ervin, then I am against the world.',
    'Ervin King',
    'Ervin Qing',
    'SES',
    'Dat Vid',
    'Ervin Feii',
    'Wat',
    'I AM Bot',
    'KONAN Is Sub-Man',
    'Konan Head is Quite Puny',
    'Rui is Man'
]



def main():

    updater = Updater(WEIKANGBOT_ID,
                    use_context=True)

    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hi, I'm Wei Bot. Write /help to see the commands available.")

    def hello(update: Update, context: CallbackContext):
        update.message.reply_text('Hello there Nerd.')

    def message(update: Update, context: CallbackContext):
        random_no = random.randint(0,len(messages)-1)
        text = messages[random_no]
        update.message.reply_text(text)

    def help(update: Update, context: CallbackContext):
        update.message.reply_text("""Available Commands :-
        /start - Start Wei
        /hello - Say Hi to Wei
        /linkedin - Get Wei's LinkedIn URL.
        /youtube - Get the link to Youtube
        /message - Get your well-customised message from Wei """)

    def youtube_url(update: Update, context: CallbackContext):
        update.message.reply_text("Youtube Link => https://www.youtube.com/watch?v=dQw4w9WgXcQ")


    def linkedIn_url(update: Update, context: CallbackContext):
        update.message.reply_text(
            "LinkedIn URL => https://www.linkedin.com/in/chong-wei-kang-246b28148/")


    def unknown(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


    def unknown_text(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('message', message))
    updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown)) # Filters out unknown commands

    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()


main()