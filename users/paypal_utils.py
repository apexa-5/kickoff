# paypal_utils.py
import requests
from django.conf import settings

def get_paypal_access_token():
    url = f'{settings.PAYPAL_BASE_URL}/v1/oauth2/token'
    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        data={'grant_type': 'client_credentials'}
    )
    return response.json()['access_token']
