import os
from dotenv import load_dotenv
from twilio.rest import Client
import pandas as pd

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


def read_table(sheet_name: str) -> pd.DataFrame:
    """
    """
    SHEET_ID = '1UuV__YRrPOeS2ccDkp0A7r5Knsyvnf_bHF2YymmVBq4'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    # Remove columns that are all NaN.
    df = df.dropna(axis=1, how='all')
    return df
