from holehe.core import *
from holehe.localuseragent import *


def wattpad(email):

    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://www.wattpad.com/',
        'TE': 'Trailers',
    }

    s.get("https://www.wattpad.com", headers=headers)
    headers["X-Requested-With"]='XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = requests.get('https://www.wattpad.com/api/v3/users/validate', headers=headers, params=params)
    if (response.status_code == 200 or response.status_code == 400):
        if response.status_code == 200:
            print(response.status_code)
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            print(response.status_code)
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        print(response.status_code)
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
