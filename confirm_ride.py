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
