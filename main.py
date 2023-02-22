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


load_dotenv()

JREMPIRE_ID = os.getenv('JREMPIRE_ID')
WEIKANGBOT_ID = os.getenv('WEIKANGBOT_ID')
WEI_TESTBOT_ID = os.getenv('WEI_TESTBOT_ID')

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
    'Rui is Man',
    'You may bring a COW...',
    'You may bring a HORSE...',
    'Rui is Man',
    'jaixer is Golden Man',
    'Rui is Half-Kane',
    'Kane is Superior',
    'FXXK Glenn',
    "Rui is a man of many talents, that's for sure!",
    'Yes, Rui is a man. What else can I help you with?',
    'Interesting. Tell me more about why you want to bring a cow or a horse.'
]

def main():

    updater = Updater(WEIKANGBOT_ID,
                    use_context=True)
    async def getQuote():
        try:
            resp = await requests.get('https://zenquotes.io/api/random')
        except:
            return "Failed to get quote! Try again later!"
        data = resp.json()
        quote = data[0]['q']
        author = data[0]['a']
        finalised_quote = (f"{quote} - {author}")
        return finalised_quote

    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hi, I'm Wei Bot. Write /help to see the commands available.")

    def hello(update: Update, context: CallbackContext):
        update.message.reply_text('Hello there Nerd.')

    def message(update: Update, context: CallbackContext):
        random_no = random.randint(0,len(messages)-1)
        text = messages[random_no]
        update.message.reply_text(text)
    
    async def quote(update: Update, context: CallbackContext):
        quote = await getQuote()
        update.message.reply_text(quote)

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

    # def userText(update:Update, context:CallbackContext):  
    #     # Function to reply to user text
    #     ai = Wit(access_token = WIT_AI_ID)
    #     resp = ai.message(update.message.text)
    #     update.message.reply_text(str(resp['intents'])[0]['name'])

    def unknown(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


    def unknown_text(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('quote', quote))
    updater.dispatcher.add_handler(CommandHandler('message', message))
    updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown)) # Filters out unknown commands

    # Filters out unknown messages.
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    #registering Message Handler to reply to user
    # updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,userText))

    updater.start_polling()


main()