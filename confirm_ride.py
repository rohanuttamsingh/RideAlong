"""
Utilities for confirming a rider and a driver.
"""

from utils import read_table, send_text


def confirm(phone_number: str):
    """
    Receives and processes a response from a rider.

    Args:
        phone_number: The phone number of the rider.
    """
    # Remove the leading +1.
    phone_number = phone_number[2:]

    # Read our database.
    user_table = read_table('Users')
    # Convert phone numbers to strings.
    user_table["Phone"] = user_table["Phone"].astype(str)
    notification_table = read_table('Notifications')

    # Find the corresponding user.
    users = user_table[user_table['Phone'] == phone_number]

    latest_notification = None
    # Find the latest notification corresponding to this user.
    for _, user in users.iterrows():
        # Get the row index of this user.
        user_index = user.name

        # Get the latest notification for this user.
        driver_notification = notification_table[notification_table["Driver Row"] == user_index]
        if len(driver_notification) > 0 and driver_notification.iloc[-1].name > latest_notification.name:
            latest_notification = driver_notification.iloc[-1]

        rider_notification = notification_table[notification_table["Rider Row"] == user_index]
        if len(rider_notification) > 0 and rider_notification.iloc[-1].name > latest_notification.name:
            latest_notification = rider_notification.iloc[-1]

    # Find if the user is a driver or a rider.
    if latest_notification["Driver Row"] == user_index:
        corider = user_table.iloc[latest_notification["Rider Row"]]
        driver = user_table.iloc[latest_notification["Driver Row"]]
        # The user is a driver.
        send_text(
            phone_number,
            f"You have confirmed a ride. Here is your corider's information: {corider.Name} is going to {corider.Destination}. Their phone number is: {corider.Phone}")
        send_text(
            corider.Phone,
            f"Your driver has matched you with a ride. {driver.Name} is going to {driver.Destination}. Their phone number is: {driver.Phone}")
    else:
        # The user is a rider.
        driver = user_table.iloc[latest_notification["Driver Row"]]
        send_text(
            driver.Phone,
            f"You have been matched with a driver. {user.Name} is going to {user.Destination}. Their phone number is: {user.Phone}. Reply 'YES' to confirm the ride."
        )
