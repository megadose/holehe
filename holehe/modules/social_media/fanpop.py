from holehe.core import *
from holehe.localuseragent import *

def fanpop(email):

    s = requests.session()

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.fanpop.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.fanpop.com/register',
    }

    data = {
      'type': 'register',
      'user[name]': '',
      'user[password]': '',
      'user[email]': email,
      'agreement': '',
      'PersistentCookie': 'PersistentCookie',
      'redirect_url': 'https://www.fanpop.com/',
      'submissiontype': 'register'
    }

    response = s.post('https://www.fanpop.com/login/superlogin', headers=headers, data=data)

    if "already registered" in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
