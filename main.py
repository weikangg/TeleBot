import os
import random
import requests
import configparser
from uuid import uuid4
from telegram.ext import CallbackQueryHandler, InlineQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram import InlineQueryResultGame
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from http.server import BaseHTTPRequestHandler

WEIKANGBOT_ID = os.environ['WEIKANGBOT_ID']
WEI_TESTBOT_ID = os.environ['WEI_TESTBOT_ID']

# Global Variables
class Global:
	def __init__(self):
		return

# Game
class GameHTTPRequestHandler(BaseHTTPRequestHandler):
	def __init__(self, *args):
		BaseHTTPRequestHandler.__init__(self, *args)

	def do_GET(self):
		if "#" in self.path:
			self.path = self.path.split("#")[0]
		if "?" in self.path:
			(route, params) = self.path.split("?")
		else:
			route = self.path
			params = ""
		route = route[1:]
		params = params.split("&")
		if route in Global.games:
			self.send_response(200)
			self.end_headers()
			self.wfile.write(open(route+'.html', 'rb').read())
		elif route == "setScore":
			params = {}
			for item in self.path.split("?")[1].split("&"):
				if "=" in item:
					pair = item.split("=")
					params[pair[0]] = pair[1]
			print(params)
			if "imid" in params:
				Global.bot.set_game_score(params["uid"], params["score"], inline_message_id=params["imid"])	
			else:
				Global.bot.set_game_score(params["uid"], params["score"], message_id=params["mid"], chat_id=params["cid"])
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'Set score')
		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(b'Invalid game!')

def main():

    # STATES
    ADDING_QUOTE, DELETING_QUOTE, CHOOSE_QUOTE = 0,0,0

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
    # INTRO STATE FOR CHOOSING CONVERSATION HANDLER
    def introChooseQuotes(update: Update, context: CallbackContext):
        update.message.reply_text('Key in the number of the quote you want to choose. Enter -1 to quit.')
        return CHOOSE_QUOTE

  # ADDING STATE FOR ADDING CONVERSATION HANDLER
    def chooseQuote(update: Update, context: CallbackContext):
        quoteNo = update.message.text
        if quoteNo == '-1':
            update.message.reply_text("Good bye.")
            return ConversationHandler.END
        try:
            quoteNo = int(quoteNo)
        except ValueError:
            update.message.reply_text("Enter the number of the quote only.")
            return CHOOSE_QUOTE
        
        if quoteNo <= 0 or quoteNo > len(db['messages']):
            update.message.reply_text("Enter the number of the quote only.")
            return CHOOSE_QUOTE
        update.message.reply_text(db['messages'][quoteNo-1])
        # return ConversationHandler.END to end the conversation
        return ConversationHandler.END 

    # INTRO STATE FOR ADDING CONVERSATION HANDLER
    def introAddMessages(update: Update, context: CallbackContext):
        update.message.reply_text('Key in a quote you want to add. Enter -1 to quit.')
        return ADDING_QUOTE

  # ADDING STATE FOR ADDING CONVERSATION HANDLER
    def addUserQuote(update: Update, context: CallbackContext):
        userQuote = update.message.text
        if userQuote == '-1':
            update.message.reply_text("Good bye.")
            return ConversationHandler.END

        returnString = f"Saving {userQuote}...."
        db['messages'].append(userQuote)
        update.message.reply_text(returnString)
        update.message.reply_text("Saved Quote.")
        # return ConversationHandler.END to end the conversation
        return ConversationHandler.END

  # INTRO STATE FOR DELETING CONVERSATION HANDLER
    def introDeleteMessages(update: Update, context: CallbackContext):
        getMessages(update,context)
        update.message.reply_text(
        'Key in the number of the quote you want to delete. Enter -1 to quit.')
        return DELETING_QUOTE

  # DELETING STATE FOR DELETING CONVERSATION HANDLER
    def deleteUserQuote(update: Update, context: CallbackContext):

        # CONVERT TO INT & ERROR HANDLING.
        try:
            userChoice = int(update.message.text)
            if userChoice == -1:
                update.message.reply_text("Good bye.")
                return ConversationHandler.END
        except ValueError:
            text = f"Enter the number of the quote you want to delete only. No playing punk. (e.g. 1 to {len(db['messages'])})\n Enter -1 to quit."
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
        del db['messages'][userChoice - 1]
        update.message.reply_text("Deleted Quote.")
        # return ConversationHandler.END to end the conversation
        return ConversationHandler.END
    
    def start(bot, update):
        bot.send_game(update.message.chat_id, Global.featured)

    def error(bot, update, error):
        print(update, error)

    def button(bot, update):
        print(update)
        query = update.callback_query
        game = query.game_short_name
        uid = str(query.from_user.id)
        if query.message:
            mid = str(query.message.message_id)
            cid = str(query.message.chat.id)
            url = "http://" + Global.host + ":"+Global.port + "/" + game + "?uid="+uid+"&mid="+mid+"&cid="+cid
        else:
            imid = update.callback_query.inline_message_id
            url = "http://" + Global.host + ":"+Global.port + "/" + game + "?uid="+uid+"&imid="+imid
        print(url)
        bot.answer_callback_query(query.id, text=game, url=url)

    def inlinequery(update, context):
        query = context.inline_query.query
        results = []
        for game in Global.games:
            if query.lower() in game.lower():
                results.append(InlineQueryResultGame(id=str(uuid4()),game_short_name=game))
        context.inline_query.answer(results)

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

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)
    Global.bot = updater.bot

    # HANDLERS FOR CONVERSATIONS
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('chooseMessage', introChooseQuotes)],
        states={
        CHOOSE_QUOTE: [MessageHandler(Filters.text, callback=chooseQuote)]
        },
        fallbacks=[CommandHandler('quit', quit)]))
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