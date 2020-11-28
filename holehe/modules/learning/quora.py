from holehe.core import *
from holehe.localuseragent import *


def quora(email):

    s = requests.session()

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://fr.quora.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    r = s.get("https://fr.quora.com", headers=headers)
    try:
        revision = r.text.split('revision": "')[1].split('"')[0]
        formkey = r.text.split('formkey": "')[1].split('"')[0]
    except:
        print("error")

    data = {
      'json': '{"args":[],"kwargs":{"value":"'+str(email)+'"}}',
      'formkey': str(formkey),
      '__hmac': '0XUlSIZzr7N1DA',
      '__method': 'validate'
    }

    response = s.post('https://fr.quora.com/webnode2/server_call_POST', headers=headers, data=data)
    try:
        if 'Un compte a' in response.text:
            return(({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None}))
        else:
            return(({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None}))
    except:
        return(({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None}))
