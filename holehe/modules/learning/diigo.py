from holehe.core import *
from holehe.localuseragent import *

def diigo(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.diigo.com/sign-up?plan=free',
    }

    s.get("https://www.diigo.com/sign-up?plan=free",headers=headers)

    headers["X-Requested-With"]='XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = s.get('https://www.diigo.com/user_mana2/check_email', headers=headers, params=params)
    if response.status_code==200:
        if response.text=="0":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

print(diigo("test@gmail.com"))
