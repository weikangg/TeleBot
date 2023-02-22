import os
import random
import requests
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

WEIKANGBOT_ID = os.environ['WEIKANGBOT_ID']
WEI_TESTBOT_ID = os.environ['WEI_TESTBOT_ID']


def main():

    # STATES
    ADDING_QUOTE, DELETING_QUOTE = 0,0

    # UPDATER
    updater = Updater(WEIKANGBOT_ID,
                    use_context=True)

    # DAILY QUOTES
    def getQuote():
        try:
            resp = requests.get('https://zenquotes.io/api/random')
        except:
            return "Failed to get quote! Try again later!"
        data = resp.json()
        quote = data[0]['q']
        author = data[0]['a']
        finalised_quote = (f"{quote} - {author}")
        return finalised_quote

    # START BOT 
    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hi, I'm Wei Bot. Write /help to see the commands available.")

    # HELLO FUNCTION
    def hello(update: Update, context: CallbackContext):
        update.message.reply_text('Hello there Nerd.')

    # SEND A RANDOM MESSAGE.
    def message(update: Update, context: CallbackContext):
        random_no = random.randint(0,len(db['messages'])-1)
        text = db['messages'][random_no]
        update.message.reply_text(text)

    # GET THE LIST OF MESSAGES
    def getMessages(update: Update, context: CallbackContext):
        messagesList = ''
        for i in range(len(db['messages'])):
          messagesList = messagesList + str(i+1) + '. '
          messagesList += db['messages'][i]
          messagesList += '\n'
        update.message.reply_text(messagesList)
      
    # INTRO STATE FOR ADDING CONVERSATION HANDLER
    def introAddMessages(update: Update, context: CallbackContext):
        update.message.reply_text('Key in a quote you want to add.')
        return ADDING_QUOTE

    # ADDING STATE FOR ADDING CONVERSATION HANDLER
    def addUserQuote(update:Update,context:CallbackContext):
      userQuote = update.message.text
      returnString = f"Saving {userQuote}...."
      db['messages'].append(userQuote)
      update.message.reply_text(returnString)
      update.message.reply_text("Saved Quote.")
      # return ConversationHandler.END to end the conversation
      return ConversationHandler.END

    # INTRO STATE FOR DELETING CONVERSATION HANDLER
    def introDeleteMessages(update: Update, context: CallbackContext):
        update.message.reply_text('Key in the number of the quote you want to delete.')
        return DELETING_QUOTE

    # DELETING STATE FOR DELETING CONVERSATION HANDLER
    def deleteUserQuote(update:Update,context:CallbackContext):

      # CONVERT TO INT & ERROR HANDLING.
      try:
        userChoice = int(update.message.text)
      except ValueError:
        text = f"Enter the number of the quote you want to delete only. No playing punk. (e.g. 1 to {len(db['messages'])}) "
        update.message.reply_text(text)
        update.message.reply_text("Let you try again.")
        return DELETING_QUOTE

      # ERROR HANDLING
      if userChoice < 1 or userChoice > len(db['messages']):
        update.message.reply_text("Dun play punk. No such quote.")
        update.message.reply_text("Let you try again.")
        return DELETING_QUOTE
      
      returnString = f"Deleting '{db['messages'][userChoice-1]}'...."
      update.message.reply_text(returnString)
      del db['messages'][userChoice-1]
      update.message.reply_text("Deleted Quote.")
      # return ConversationHandler.END to end the conversation
      return ConversationHandler.END
      
    # QUIT STATE FOR CONVERSATION HANDLERS
    def quit(update:Update,context:CallbackContext):
      update.message.reply_text('Saved Quote.')
      return ConversationHandler.END

    # GET REAL INSPIRATIONAL QUOTES
    def quote(update: Update, context: CallbackContext):
        quote = getQuote()
        update.message.reply_text(quote)

    # HELP FUNCTION
    def help(update: Update, context: CallbackContext):
        update.message.reply_text("""Available Commands :
        /start - Start Wei
        /hello - Say Hi to Wei
        /linkedin - Get Wei's LinkedIn URL.
        /youtube - Get the link to Youtube
        /quote - Get your daily quote from Wei
        /message - Get your well-customised message from Wei
        /getmessages - Get the full list of customised messages from Wei
        /addmessages - Add your customised message to Wei
        /deletemessages - Delete a message of your choice from Wei
        """)

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

    # HANDLE UNKNOWN COMMANDS
    def unknown(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)

    # HANDLERS FOR CONVERSATIONS
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('addmessages', introAddMessages)],
        states={
            ADDING_QUOTE: [MessageHandler(Filters.text, callback=addUserQuote)]
        },
        fallbacks=[CommandHandler('quit', quit)]
    ))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('deletemessages', introDeleteMessages)],
        states={
            DELETING_QUOTE: [MessageHandler(Filters.text, callback=deleteUserQuote)]
        },
        fallbacks=[CommandHandler('quit', quit)]
    ))

    # HANDLERS FOR COMMANDS
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('quote', quote))
    updater.dispatcher.add_handler(CommandHandler('message', message))
    updater.dispatcher.add_handler(CommandHandler('getmessages', getMessages))
    updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown)) # Filters out unknown commands


    updater.start_polling()

main()