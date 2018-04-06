import json
from jose import jwt

def get_pem(fname):
    with open(fname, 'r') as f:
        return f.read()

PRIV_KEY = get_pem('keys/benwaonline_api_test_priv.pem')
PUB_KEY = get_pem('keys/benwaonline_api_test_pub.pem')

def generate_jwt(claims):
    ''' Generates a JWT'''
    headers = {
        'typ': 'JWT',
        'alg': 'RS256',
        'kid': 'benwaonline_api_test'
    }
    return jwt.encode(claims, PRIV_KEY, algorithm='RS256', headers=headers)
