from holehe.core import *
from holehe.localuseragent import *


def redtube(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://redtube.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    r=s.get("https://redtube.com/register",headers=headers)
    soup=BeautifulSoup(r.text,features="html.parser")
    try:
        token=soup.find(attrs={"id":"token"}).get("value")
        if token==None:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    headers['X-Requested-With']= 'XMLHttpRequest'


    params = (
        ('token', token),
    )

    data = {
      'token': token,
      'redirect': '',
      'check_what': 'email',
      'email': email
    }

    response = s.post('https://www.redtube.com/user/create_account_check', headers=headers, params=params, data=data)

    if "Email has been taken." in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
