from holehe.core import *
from holehe.localuseragent import *


def lastpass(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://lastpass.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    params = (
        ('check', 'avail'),
        ('skipcontent', '1'),
        ('mistype', '1'),
        ('username', email),
    )

    response = requests.get(
        'https://lastpass.com/create_account.php',
        params=params,
        headers=headers)
    if response.text == "no":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    if response.text == "ok" or response.text == "emailinvalid":
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
