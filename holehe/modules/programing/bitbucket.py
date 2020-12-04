from holehe.core import *
from holehe.localuseragent import *

def bitbucket(email):
    headers = {
        'authority': 'id.atlassian.com',
        'user-agent': random.choice(ua["browsers"]["chrome"]),
        'dnt': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://id.atlassian.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://id.atlassian.com/',
        'accept-language': 'es,en-US;q=0.9,en;q=0.8',
        'sec-gpc': '1',
    }

    data = {
      'username': email
    }

    response = requests.post('https://id.atlassian.com/rest/check-username', headers=headers, data=data)

    if 'signup' in response.text:
        return ({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return ({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
