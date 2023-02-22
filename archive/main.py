# Step 1: Create telegram group in which you will send messages
# Step 2: Create Telegram Bot using BotFather & Add Bot in the group
# Step 3: Get the updates and chatID. Using Bot HTTP code given from BotFather
#   https://api.telegram.org/bot6295136362:AAHBDh_sHPYGDhU0c58IyWK3UqFmnoY0bAA/getUpdates
# Step 4: Chat ID (-1001899096479)
# Step 5: Send a message.
#   https://api.telegram.org/bot5892449449:AAFR5MOpaNLavNQF1M9zpD216Ue1mU-sSz8/sendMessage?chat_id=-840851884&text='This is a test message'
# Chat ID : 


import requests
import random
import time
import os
from dotenv import load_dotenv

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
    'Rui is Man',
    'jaixer is Golden Man'
]

# JR EMPIRE
# random_no = random.randint(0,len(messages)-1)
# text = 'Haii'
# base_url = f'https://api.telegram.org/bot{WEIKANGBOT_ID}/sendMessage?chat_id={JREMPIRE_ID}&text={text}'
# resp = requests.get(base_url)
# print(resp.text)

## LOOP

# while True:
#     random_no = random.randint(0,len(messages)-1)
#     base_url = f'https://api.telegram.org/bot6295136362:AAHBDh_sHPYGDhU0c58IyWK3UqFmnoY0bAA/sendMessage?chat_id=-1001899096479&text={messages[random_no]}'
#     requests.get(base_url)
#     time.sleep(5)


## RANDOM GROUPS
# random_no = random.randint(0,len(messages)-1)
# base_url = f'https://api.telegram.org/bot6295136362:AAHBDh_sHPYGDhU0c58IyWK3UqFmnoY0bAA/sendMessage?chat_id=-536082569&text=Hello'
# requests.get(base_url)


### RESPOND TO MESSAGES
# base_url = f'https://api.telegram.org/bot{WEIKANGBOT_ID}/getUpdates'
# resp = requests.get(base_url)
# data = resp.json()

# for item in data['result']:
#     try:
#         if item['message']['entities'][0]['type'] == 'mention':
#             chat_id = item['message']['chat']['id']
#             user_id = item['message']['from']['id']
#             user_name = item['message']['from']['username'] 
#             message = item['message']['text']

#             if 'hi' or 'hello' in message.lower():

#                 text = f'''
#                 <a href = "tg://user?id={user_id}">@{user_name}></a>
#                 Hi, how are you doing? Let me know if you need aid.
#                 '''
#                 to_url = f'https://api.telegram.org/bot{WEIKANGBOT_ID}/sendMessage?chat_id={JREMPIRE_ID}&text={text}&parse_mode=HTML'
#                 resp = requests.get(to_url)
#         elif item['message']['entities'][0]['type'] == 'bot_command':
#             chat_id = item['message']['chat']['id']
#             user_id = item['message']['from']['id']
#             user_name = item['message']['from']['username'] 
#             message = item['message']['text']

#             if 'hi' or 'hello' in message.lower():

#                 text = f'''
#                 <a href = "tg://user?id={user_id}">@{user_name}></a>
#                 Wat
#                 '''
#                 to_url = f'https://api.telegram.org/bot{WEIKANGBOT_ID}/sendMessage?chat_id={JREMPIRE_ID}&text={text}&parse_mode=HTML'
#                 resp = requests.get(to_url)
#         else:
#             pass
#     except:
#         pass
