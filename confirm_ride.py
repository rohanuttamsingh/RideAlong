"""
Utilities for confirming a rider and a driver.
"""

def handle_rider_response(phone_number: str, body: str):
    """
    Receives and processes a response from a rider.
    
    Args:
        phone_number: The phone number of the rider.
        body: The body of the rider's response.
    """
    if body.capitalize() != 'Yes':
        return

    # If confirmed, send a text to the driver.
    

def handle_driver_response(phone_number: str, body: str):
    """
    Receives and processes a response from a driver.
    
    Args:
        phone_number: The phone number of the driver.
        body: The body of the driver's response.
    """
    # If confirmed, send a text to both the rider and the driver.

