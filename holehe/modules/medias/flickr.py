from holehe.core import *
from holehe.localuseragent import *


def flickr(email):
    url = "https://identity-api.flickr.com/migration"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://identity.flickr.com/login',
        'Origin': 'https://identity.flickr.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    params = (
        ('email', email),
    )
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data['state_code'] == '5':
        return ({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return ({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
