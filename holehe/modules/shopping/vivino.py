from holehe.core import *
from holehe.localuseragent import *

def vivino(email):
    s = requests.session()


    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.vivino.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r = s.get("https://www.tunefind.com/user/join", headers=headers)
    try:
        crsf_token = r.text.split('"csrf-token" content="')[1].split('"')[0]
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    headers['X-CRSF-Token'] = crsf_token
    data = '{"email":"'+str(email)+'","password":"e"}'

    response = s.post('https://www.vivino.com/api/login', headers=headers, data=data)
    if response.status_code == 429:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        if response.json()['error'] == "The supplied email does not exist":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
