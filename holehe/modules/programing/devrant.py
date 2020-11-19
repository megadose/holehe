from holehe.core import *
from holehe.localuseragent import *



def devrant(email):

    s = requests.session()

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://devrant.com',
        'Connection': 'keep-alive',
        'Referer': 'https://devrant.com/feed/top/month?login=1',
    }

    data = {
      'app': '3',
      'type': '1',
      'email': email,
      'username': '',
      'password': '',
      'guid': '',
      'plat': '3',
      'sid': '',
      'seid': ''
    }

    response = s.post('https://devrant.com/api/users', headers=headers, data=data)
    result = response.json()['error']
    if result == 'The email specified is already registered to an account.':
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
