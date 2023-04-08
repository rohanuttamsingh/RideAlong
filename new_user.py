from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import datetime
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from utils import send_text
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
    date: datetime.date

def get_users() -> pd.DataFrame:
    SHEET_ID = '1UuV__YRrPOeS2ccDkp0A7r5Knsyvnf_bHF2YymmVBq4'
    SHEET_NAME = 'Users'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)
    df = df[['School', 'Destination', 'Type', 'Seats', 'Phone', 'Name', 'Date']]
    return df

def create_user_from_row(row) -> User:
    type = Type.RIDER if row['Type'] == 'Rider' else Type.DRIVER
    seats = row['Seats'] if not pd.isna(row['Seats']) else None
    date_list = row['Date'].split('/')
    month, day, year = map(lambda i: int(i), date_list)
    year += 2000
    date = datetime.date(year, month, day)
    return User(type, row['Name'], row['Phone'], row['School'], row['Destination'], seats, date)

def get_users_list() -> List[User]:
    users_df = get_users()
    users_list = []
    users_df.apply(lambda u: users_list.append(create_user_from_row(u)), 1)
    return users_list

def handle_new_user():
    """When a user requests or offers a ride, find a user of the opposite type from their university
    going the closest to their destination."""
    users = get_users_list()
    user = users[-1]
    users = users[:-1]
    # Possible matches are the opposite type, from same university, and are traveling within 1 day
    cond = lambda u: u.type != user.type and u.university == user.university and abs((u.date - user.date).days) <= 1
    possible_matches = list(filter(cond, users))
    match_destinations = [match.destination for match in possible_matches]
    distance_matrix = get_distance_matrix(user.destination, match_destinations)
    durations = [el['duration']['value'] for el in distance_matrix['rows'][0]['elements']]
    idx, min_duration = 0, durations[0]
    for i, duration in enumerate(durations):
        if duration < min_duration:
            idx, min_duration = i, duration
    if min_duration > 60: # No matches within 1 hour
        return
    else:
        match = possible_matches[idx]
        minutes = duration // 60
        # text_match(user, match, minutes)
        # text_match(match, user, minutes)
        print(user, match, minutes)

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

# print(handle_new_user(User(Type.RIDER, 'Test', '123', 'UMD', 'New York, NY', None)))
# handle_new_user(User(Type.RIDER, 'Rider', '4435406776', 'UMD', 'New York, NY', None))
# handle_new_user(User(Type.RIDER, 'Rider', '4435406776', 'UMD', 'Scranton, PA', None))
# print(get_users())
# print(get_users_list())
