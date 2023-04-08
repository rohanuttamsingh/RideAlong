import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]

def get_distance(university, destination):
    """
    Returns the time in seconds for to get from one location to another using the google maps API.
    """

    # Get the distance from the google maps API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format('%7C'.join(university), '%7C'.join(destination), API_KEY)
    response = requests.get(url)
    data = response.json()
    return data
    distance = data['rows'][0]['elements'][0]['duration']['value']

    return distance

print(get_distance(["University of California, Berkeley", "Stanford University"], ["San Francisco, CA", "College Park, MD"]))
