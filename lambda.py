import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
API_KEY = os.environ["API_KEY"]
ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

SCHOOL_ABBREVIATION_TO_NAME = {
    "UMD": "University of Maryland, College Park",
    "UMBC": "University of Maryland, Baltimore County",
    "UVA": "University of Virginia",
    "GW": "George Washington University",
    "JHU": "Johns Hopkins University",
    "Towson": "Towson University",
    "American": "American University",
    "Howard": "Howard University",
    "Georgetown": "Georgetown University",
    "UMES": "University of Maryland Eastern Shore",
    "Salisbury": "Salisbury University",
}

def get_distance(university, destination):
    """
    Returns the time in seconds for to get from one location to another using the google maps API.
    """

    university = SCHOOL_ABBREVIATION_TO_NAME.get(university, university)

    # Get the distance from the google maps API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format('%7C'.join(university), '%7C'.join(destination), API_KEY)
    response = requests.get(url)
    data = response.json()
    return data
    distance = data['rows'][0]['elements'][0]['duration']['value']

    return distance

def send_text(number, message):
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

print(get_distance(["University of California, Berkeley", "Stanford University"], ["San Francisco, CA", "College Park, MD"]))
send_text("+16677015404", "Hi, from twilio and bitcamp")