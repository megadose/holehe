from holehe.core import *
from holehe.localuseragent import *



def blip(email):

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://blip.fm',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://blip.fm/',
    }

    data = {
      'referringUrl': '',
      'genpass': '1',
      'signup[urlName]': 'test',
      'signup[emailAddress]': email,
      'g-recaptcha-response': '',
      'tos': '0'
    }
    try:
        response = requests.post('https://blip.fm/signup/save', headers=headers, data=data)
        if 'That email address is already in use.' in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif 'cloudfront.net/images/blip/spinner.gif" alt="loading..."' in response.text:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
