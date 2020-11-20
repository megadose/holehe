import requests

def bodybuilding(email):
    headers = {
    'User-Agent': random.choice(ua["browsers"]["firefox"]),
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,en-US;q=0.5',
    'Origin': 'https://www.bodybuilding.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.bodybuilding.com/',
    }

    response = requests.head('https://api.bodybuilding.com/profile/email/teezt@gmail.com', headers=headers)
    if response.status_code==200:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
