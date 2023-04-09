from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import datetime
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]
ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

class Type(Enum):
    RIDER = 1
    DRIVER = 2

@dataclass
class User:
    row: int
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
    if not pd.isna(row['Date']):
        date_list = row['Date'].split('/')
        month, day, year = map(lambda i: int(i), date_list)
        year += 2000
        date = datetime.date(year, month, day)
    else:
        date = None
    return User(row.name, type, row['Name'], row['Phone'], row['School'], row['Destination'], seats, date)


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
    # Possible matches are the opposite type and are from same university
    cond = lambda u: u.type != user.type and u.university == user.university
    possible_matches = list(filter(cond, users))
    match_destinations = [match.destination for match in possible_matches]
    distance_matrix = get_distance_matrix(user.destination, match_destinations)
    durations = []
    for el in distance_matrix['rows'][0]['elements']:
        if el['status'] == 'ZERO_RESULTS':
            durations.append(None)
        else:
            durations.append(el['duration']['value'])
    idx, min_duration = 0, durations[0]
    for i, duration in enumerate(durations):
        if duration is not None and duration < min_duration:
            idx, min_duration = i, duration
    if min_duration is None or min_duration > 60 * 60: # No matches within 1 hour
        print('No match found')
        return
    else:
        print('Match found')
        match = possible_matches[idx]
        if user.type == Type.RIDER:
            rider, driver = user, match
        else:
            rider, driver = match, user
        minutes = duration // 60
        message = f'{rider.name}, CoRide found a match!'
        message += f' {driver.name} is driving on {driver.date} to {driver.destination}, which is only {minutes} minutes away from your destination, {rider.destination}.'
        message += f' Reply with YES to confirm this CoRide.'
        number = f"+1{rider.phone}"
        send_request(message, number)
        requests.post("https://hooks.zapier.com/hooks/catch/13745389/32g4uuy/", json={
            "rider_row": rider.row,
            "driver_row": driver.row,
        })

def get_distance_matrix(origin: str, destinations: List[str]):
    """
    Returns the time in seconds for to get from one location to another using the google maps API.
    """
    # Get the distance from the google maps API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format(origin, '%7C'.join(destinations), API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

def send_request(message, to_number):
    url = f'https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_TOKEN}/Messages.json'
    payload = {
        'Body': message,
        'From': '+18339642490',
        'To': to_number
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, auth=(ACCOUNT_TOKEN, AUTH_TOKEN))
    print(response.text)

def lambda_handler(*args, **kwargs):
    handle_new_user()
