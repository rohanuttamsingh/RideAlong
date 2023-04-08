import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

def send_text(number: str, message: str):
    """
    Sends a text message to number with body message
    Number must be a string and have +1 in front of it
    ex. +16677015404
    """
    client = Client(ACCOUNT_TOKEN, AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_="+18339642490",
        to=number
    )
    print(message.sid)