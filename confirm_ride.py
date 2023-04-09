"""
Utilities for confirming a rider and a driver.
"""

from utils import read_table
from new_user import send_request


def confirm(event, _):
    """
    Receives and processes a response from a rider.

    Params:
        phone: The phone number of the rider.
    """
    phone_number = event['phone']
    # Remove the leading +1.
    if "+1" in phone_number:
        phone_number = phone_number[2:]

    # Read our database.
    user_table = read_table('Users')
    # Convert phone numbers to strings.
    user_table["Phone"] = user_table["Phone"].astype(str)
    notification_table = read_table('Notifications')

    # Find the corresponding user.
    users = user_table[user_table['Phone'] == phone_number]

    latest_notification = {
        "name": -1,
    }
    # Find the latest notification corresponding to this user.
    for _, user in users.iterrows():
        # Get the row index of this user.
        user_index = user.name

        # Get the latest notification for this user.
        driver_notification = notification_table[notification_table["Driver Row"] == user_index]
        if len(driver_notification) > 0 and driver_notification.iloc[-1].name > latest_notification["name"]:
            latest_notification = driver_notification.iloc[-1]

        rider_notification = notification_table[notification_table["Rider Row"] == user_index]
        if len(rider_notification) > 0 and rider_notification.iloc[-1].name > latest_notification["name"]:
            latest_notification = rider_notification.iloc[-1]

    if "Driver Row" not in latest_notification:
        print("No matching notification found.")
        return

    # Find if the user is a driver or a rider.
    if latest_notification["Driver Row"] == user_index:
        # The user is a driver.
        corider = user_table.iloc[latest_notification["Rider Row"]]
        driver = user_table.iloc[latest_notification["Driver Row"]]

        send_request(
            f"You have confirmed a ride. Here is your corider's information: {corider.Name} is going to {corider.Destination}. Their phone number is: {corider.Phone}",
            driver.Phone
        )
        send_request(
            f"Your driver has accepted your ride. {driver.Name} is going to {driver.Destination}. Their phone number is: {driver.Phone}",
            corider.Phone
        )
    else:
        # The user is a rider.
        corider = user_table.iloc[latest_notification["Rider Row"]]
        driver = user_table.iloc[latest_notification["Driver Row"]]

        send_request(
            f"{corider.Name} is interested in a ride. They're going to {corider.Destination}. Reply with 'YES' to confirm.",
            driver.Phone
        )
