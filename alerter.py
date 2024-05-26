"""
    Equistonic // May 2024
"""

# Imports
from decouple import config
import requests

#  Webhook Setup
WEBHOOK = config('WEBHOOK')

# Color Constants
STATUS_COLORS = {
    'error': 'FF0000',
    'warning': 'FE9A22',
    'critical': '550000',
    'notification': 'CCCCFF'
}

# Functions
def hex_to_decimal(hex: str):
    """Takes in a hexidecimal as a string  and converts it to a decimal number.

    Args:
        hex (str): The hexidecimal to convert

    Returns:
        integer: The converted hexidecimal
    """

    chars = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    hex_len = len(hex) - 1
    num = 0

    for i in range(len(hex)):
        char = hex[i]
        if char in chars.keys():
            num += chars.get(char) * (16 ** (hex_len - i))
        else:
            num += int(char) * (16 ** (hex_len - i))
    return num


def generate_embed(title: str, color: int, *fields: dict):
    """Generates an embed field for the webhook object.

    Args:
        title (str): Title of the embed
        color (int): Color of the embed
        fields (dict): Embed fields {'name': '', 'value': '', 'inline': 'true'}

    Returns:
        _type_: _description_
    """

    return {
        'title': title,
        'color': color,
        'fields': fields
    }


def parse_message(content: str, origin: str, embeds: list):
    return {
        'content': content,
        'username': origin,
        'embeds': embeds
    }


def post_message(message: dict):
    """Sends a POST request to the Discord Webhook with the given message JSON.

    Args:
        message (dict): The message data to be posted.
    """

    response = requests.post(
        WEBHOOK,
        json=message
    )
    
    if response.status_code == 200 or response.status_code == 204:
        print('Message posted successfully.')
    else:
        print(f'Failed to post message. Status code: {response.status_code}, Response: {response.text}')


if __name__ == "__main__":
    embeds = []
    embeds.append(generate_embed('**Embeds**', hex_to_decimal(STATUS_COLORS.get('warning')), {'name': 'Embed 1', 'value': 'Description', 'inline': 'true'}, {'name': 'Embed 2', 'value': 'Statistics', 'inline': 'true'}))
    message = parse_message(
        '',
        '<eq> Alerter',
        embeds
    )
    
    post_message(message)