from dataclasses import dataclass
from enum import Enum
from typing import Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]

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
    User(Type.DRIVER, 'Ryan', '8888888888', 'UMD', 'Columbia, MD', 2),
    User(Type.DRIVER, 'TicketMaster', '9999999999', 'UMD', 'New York, NY', 3),
    User(Type.DRIVER, 'OpenTicket', '2222222222', 'UMD', 'Salisbury, MD', 1),
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
    return possible_matches[idx]

def get_distance_matrix(origin, destinations):
    """
    Returns the time in seconds for to get from one location to another using the google maps API.
    """
    # Get the distance from the google maps API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format(origin, '%7C'.join(destinations), API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

# print(get_distance(["University of California, Berkeley", "Stanford University"], ["San Francisco, CA", "College Park, MD"]))
print(handle_new_user(User(Type.RIDER, 'Test', '123', 'UMD', 'New York, NY', None)))
