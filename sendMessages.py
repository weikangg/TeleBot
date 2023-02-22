# Step 1: Create telegram group in which you will send messages
# Step 2: Create Telegram Bot using BotFather & Add Bot in the group
# Step 3: Get the updates and chatID. Using Bot HTTP code given from BotFather
#   https://api.telegram.org/bot<BOTID>/getUpdates
# Step 4: Chat ID (<GET CHAT ID>)
# Step 5: Send a message.
#   https://api.telegram.org/bot<BOT_ID>/sendMessage?chat_id=<CHAT_ID>&text='This is a test message'
# Chat ID : 

import requests
import os
from dotenv import load_dotenv

load_dotenv()

JREMPIRE_ID = os.getenv('JREMPIRE_ID')
WEIKANGBOT_ID = os.getenv('WEIKANGBOT_ID')

# JR EMPIRE
text = 'Do you like my quotes?'
base_url = f'https://api.telegram.org/bot{WEIKANGBOT_ID}/sendMessage?chat_id={JREMPIRE_ID}&text={text}'
resp = requests.get(base_url)
print(resp.text)

