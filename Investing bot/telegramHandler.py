import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import telegram


"""
Function that takes as input:
    username: the username of the bot, user or even channel
    msg: the message to send
and that uses telethon package to auto-send message.
"""
def send_message_telethon(username, msg):
    # app parameters
    api_id = 3135585
    api_hash = '99ce8210aaa6ecb357ce43a0e701fda4'

    phone = '+32472815219'

    # telegram session creation
    client = TelegramClient('session', api_id, api_hash)

    client.connect()

    # first connection handling
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input("Enter the code: "))

    try:
        receiver = client.get_input_entity(username)
        client.send_message(entity=receiver, message=msg)
    except Exception as e:
        print(e)

    client.disconnect()


"""
Function that takes as input:
    token: the token of the bot
    chat_id: the id of the conversation
    msg: the message to send
and that uses python-telegram-bot package to send bot message into specific conversation
"""
def send_message_telegram_bot(token, chat_id, msg):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)






