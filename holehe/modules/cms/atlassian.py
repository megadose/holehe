from holehe.core import *
from holehe.localuseragent import *
from bs4 import BeautifulSoup

from holehe.core import *

def atlassian(email):

    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://id.atlassian.com/',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://id.atlassian.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    r=s.get("https://id.atlassian.com/login",headers=headers)
    try:
        data = {
          'csrfToken': r.text.split('{&quot;csrfToken&quot;:&quot;')[1].split('&quot')[0],
          'username': email
        }
    except :
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    response = requests.post('https://id.atlassian.com/rest/check-username', headers=headers, data=data)
    if response.json()["action"]=="signup":
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
