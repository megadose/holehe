from holehe.core import *
from holehe.localuseragent import *


def caringbridge(email):
    cookies = {
        'lang': 'en_US',
        'showSurvey': 'true',
        'cookiesEnabled': 'true',
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.caringbridge.org',
        'Connection': 'keep-alive',
        'Referer': 'https://www.caringbridge.org/signin',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }

    data = {
      'csrf': '',
      'email': email,
      'password_placeholder': '',
      'submit-btn': 'Continue'
    }

    response = requests.post('https://www.caringbridge.org/signin', headers=headers, cookies=cookies, data=data)
    if "Welcome Back,"in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
