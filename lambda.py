from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
API_KEY = os.environ["API_KEY"]
ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

class Type(Enum):
    RIDER = 1
    DRIVER = 2

@dataclass
class User:
    type: Type
    name: str
    phone: str
    university: str
    destination: str
    seats: Optional[int]

users = [
    User(Type.RIDER, 'Rohan', '4435406776', 'UMD', 'Fulton, MD', None),
    User(Type.RIDER, 'Peter', '8472120384', 'UMD', 'Salisbury, MD', None),
    User(Type.RIDER, 'Abhi', '1234567890', 'UMD', 'Ellicott City, MD', None),
    User(Type.RIDER, 'Bryan', '0987654321', 'UMD', 'Philadelphia, PA', None),
    User(Type.DRIVER, 'Ryan', '4435406776', 'UMD', 'Columbia, MD', 2),
    User(Type.DRIVER, 'TicketMaster', '4435406776', 'UMD', 'New York, NY', 3),
    User(Type.DRIVER, 'OpenTicket', '4435406776', 'UMD', 'Salisbury, MD', 1),
]


def handle_new_user(user: User):
    """When a user requests or offers a ride, find a user of the opposite type from their university
    going the closest to their destination."""
    # Possible matches are the opposite type and from same university
    possible_matches = list(filter(lambda u: u.type != user.type and u.university == user.university, users))
    match_destinations = [match.destination for match in possible_matches]
    distance_matrix = get_distance_matrix(user.destination, match_destinations)
    durations = [el['duration']['value'] for el in distance_matrix['rows'][0]['elements']]
    idx, min_duration = 0, durations[0]
    for i, duration in enumerate(durations):
        if duration < min_duration:
            idx, min_duration = i, duration
    if min_duration > 60: # No matches within 1 hour
        return
    match = possible_matches[idx]
    minutes = duration // 60
    text_match(user, match, minutes)
    text_match(match, user, minutes)

def get_distance_matrix(origin: str, destinations: List[str]):
    """
    Returns the time in seconds for to get from one location to another using the google maps API.
    """
    # Get the distance from the google maps API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format(origin, '%7C'.join(destinations), API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

def text_match(user: User, match: User, minutes: int):
    message = f'{user.name}, CoRide found a match!'
    if match.type == Type.DRIVER:
        action = 'is driving'
    else:
        action = 'needs a ride'
    message += f' {match.name} {action} to {match.destination}, which is only {minutes} away from your destination, {user.destination}.'
    message += f' Connect with {match.name} at {match.phone}.'
    number = '+1' + user.phone
    send_text(number, message)

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

# print(handle_new_user(User(Type.RIDER, 'Test', '123', 'UMD', 'New York, NY', None)))
handle_new_user(User(Type.RIDER, 'Rider', '4435406776', 'UMD', 'New York, NY', None))
handle_new_user(User(Type.RIDER, 'Rider', '4435406776', 'UMD', 'Scranton, PA', None))
