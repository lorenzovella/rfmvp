from twilio.rest import Client
from os import environ
import telegram_send


def sendMessageT(body):
    telegram_send.send(conf="telegramConf",messages=[body] )

def sendMessageW(body, number):
    account_sid = environ.get('twillio_sid')
    auth_token = environ.get('twillio_token')
    number = str('whatsapp:+55'+number)
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body,from_='whatsapp:+16106162363',to=number)
    print(message.sid)
