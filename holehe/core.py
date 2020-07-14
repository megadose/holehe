import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

def adobe(email):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.chrome,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-IMS-CLIENTID': 'adobedotcom2',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://auth.services.adobe.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"username":"'+email+'","accountType":"individual"}'
    r =requests.post('https://auth.services.adobe.com/signin/v1/authenticationstate', headers=headers, data=data).json()
    if "errorCode" in str(r.keys()):
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    headers = {
        'User-Agent': ua.chrome,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-IMS-CLIENTID': 'adobedotcom2',
        'X-IMS-Authentication-State': r['id'],
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    params = (
        ('purpose', 'passwordRecovery'),
    )
    response = requests.get('https://auth.services.adobe.com/signin/v2/challenges', headers=headers, params=params).json()
    return({"rateLimit":False,"exists":True,"emailrecovery":response['secondaryEmail'],"phoneNumber":response['securityPhoneNumber'],"others":None})
def ebay(email):
    ua = UserAgent()
    s = requests.session()
    s.headers = {
        'User-Agent': ua.chrome,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        srt=s.get("https://www.ebay.com/signin/").text.split('"csrfAjaxToken":"')[1].split('"')[0]
    except IndexError as e:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":None})

    data = {
      'identifier': email,
      'srt': srt
    }

    response = s.post('https://signin.ebay.com/signin/srv/identifer', data=data).json()
    if "err" in response.keys():
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
def apple(email):
    import requests
    s = requests.session()

    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    params = (
        ('language', 'en_US'),
    )

    response = s.get('https://iforgot.apple.com/password/verify/appleid', params=params)
    sstt=response.text.split('sstt: encodeURIComponent("')[1].split('"')[0]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/json',
        'sstt': sstt,
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://iforgot.apple.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://iforgot.apple.com/password/verify/appleid?language=en_US',
    }

    data = '{"id":"'+email+'"}'

    response = s.post('https://iforgot.apple.com/password/verify/appleid', headers=headers, data=data)
    try:
        response.json()['sstt']
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    except KeyError as e:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def facebook(email):
    s = requests.Session()
    req = s.get('https://www.facebook.com/login/identify?ctx=recover&lwv=110')
    token = re.findall(r'"token":"([a-zA-Z0-9_-]+)"', req.text)[0]
    if not token:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":{"FullName":None,"profilePicture":None}})

    pattern = r'"_js_datr","([a-zA-Z0-9_-]+)"'
    jsdatr = re.findall(pattern, req.text)[0]
    if not jsdatr:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":{"FullName":None,"profilePicture":None}})

    data = {'lsd': token,
            'email': email,
            'did_submit': 'Search',
            '__user': 0,
            '__a': 1}
    cookies = {'_js_datr': jsdatr + ';'}
    headers = {'referer': 'https://www.facebook.com/login/identify?ctx=recover&lwv=110'}
    req = s.post('https://www.facebook.com/ajax/login/help/identify.php?ctx=recover', cookies=cookies, data=data, headers=headers)

    pattern = r'ldata=([a-zA-Z0-9-_]+)\\"'
    try:
        ldata = re.findall(pattern, req.text)[0]
    except IndexError:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":{"FullName":None,"profilePicture":None}})
    if not ldata:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":{"FullName":None,"profilePicture":None}})

    req = s.get('https://www.facebook.com/recover/initiate?ldata=%s' % ldata)
    soup = BeautifulSoup(req.content,features="lxml")
    full_name = soup.find('div', attrs={'class': 'fsl fwb fcb'})
    profile_picture = soup.find('img', attrs={'class': 'img'}).get("src")
    try:
        emailrecovery = req.text.split('</strong><br /><div>')[1].split("</div>")[0].replace("&#064;","@")
        if emailrecovery==email:
            emailrecovery=None

    except IndexError:
        emailrecovery=None
    try:
        phone = req.text.split('</strong><br /><div dir="ltr">+')[1].split("</div>")[0]
    except IndexError:
        phone=None
    if full_name == None:
        full_name = ""
    else:
        if full_name != email:
            full_name = full_name.text

    return({"rateLimit":False,"exists":True,"emailrecovery":emailrecovery,"phoneNumber":phone,"others":{"FullName":full_name,"profilePicture":profile_picture}})
def instagram(email):
    ua = UserAgent()
    s = requests.session()
    s.headers = {
        'User-Agent': ua.chrome,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    try:
        freq=s.get("https://www.instagram.com/accounts/emailsignup/")
        token= freq.cookies["csrftoken"]
        check = s.post("https://www.instagram.com/accounts/web_create_ajax/attempt/",data={"email": email},headers={"x-csrftoken": token}).json()
        if check["errors"]["email"][0]["code"]=="email_is_taken":
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    except:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def tumblr(email):
    ua = UserAgent()
    s = requests.session()

    s.headers = {
        'User-Agent': ua.chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    firstreq=s.get("https://www.tumblr.com/login")
    #print(firstreq.text)
    data = [
      ('determine_email', email),
      ('user[email]', ''),
      ('user[password]', ''),
      ('tumblelog[name]', ''),
      ('user[age]', ''),
      ('context', 'no_referer'),
      ('version', 'STANDARD'),
      ('follow', ''),
      ('form_key', firstreq.text.split('<meta name="tumblr-form-key" id="tumblr_form_key" content="')[1].split('"')[0]),
      ('seen_suggestion', '0'),
      ('used_suggestion', '0'),
      ('used_auto_suggestion', '0'),
      ('about_tumblr_slide', ''),
      ('random_username_suggestions', firstreq.text.split('id="random_username_suggestions" name="random_username_suggestions" value="')[1].split('"')[0]),
      ('action', 'signup_determine'),
      ('action', 'signup_determine'),
      ('tracking_url', '/login'),
      ('tracking_version', 'modal'),
    ]

    response = s.post('https://www.tumblr.com/svc/account/register', data=data)
    if response.text=='{"redirect":false,"redirect_method":"GET","errors":[],"signup_success":false,"next_view":"signup_magiclink"}':
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def pastebin(email):
    req = requests.post("https://pastebin.com/ajax/check_email.php",data={"action": "check_email", "username": email})
    regex = re.compile(r"^<font color=\"(red|green)\">([^<>]+)<\/font>$")
    verif = regex.match(req.text)
    if '<font color="red">' in str(verif):
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    if '<font color="green">' in str(verif):
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":None})

def github(email):
    ua = UserAgent()
    s = requests.session()
    freq = s.get("https://github.com/join")
    token_regex = re.compile(r'<auto-check src="/signup_check/username[\s\S]*value="([\S]*)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*value="([\S]*)"[\s\S]*</auto-check>')
    token = re.findall(token_regex,freq.text)
    data={"value": email, "authenticity_token": token[0]}
    #print(data)
    req = s.post("https://github.com/signup_check/email",data=data)
    if "Your browser did something unexpected." in req.text:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":None})
    if req.status_code==422:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    if req.status_code==200:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":None})
def twitter(email):
    req = requests.get("https://api.twitter.com/i/users/email_available.json",params={"email": email})
    if str(req.json()["taken"])=="True":
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def pinterest(email):
    req = requests.get("https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",params={"source_url": "/", "data": '{"options": {"email": "'+email+'"}, "context": {}}'})
    if req.json()["resource_response"]["data"]:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def lastfm(email):
    req = requests.get("https://www.last.fm/join")
    token = req.cookies["csrftoken"]
    data = {"csrfmiddlewaretoken": token, "userName": "", "email": email}
    headers = {
        "Accept": "*/*",
        "Referer": "https://www.last.fm/join",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"csrftoken={token}",
    }
    check = requests.post("https://www.last.fm/join/partial/validate",headers=headers,data=data).json()
    if check["email"]["valid"]:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
def spotify(email):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.chrome,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = (
        ('validate', '1'),
        ('email', email),
    )

    req = requests.get('https://spclient.wg.spotify.com/signup/public/v1/account', headers=headers, params=params)
    if req.json()["status"] == 1:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif req.json()["status"] == 20:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":None,"emailrecovery":None,"phoneNumber":None,"others":None})
def firefox(email):
    req = requests.post("https://api.accounts.firefox.com/v1/account/status",data={"email": email})
    if "false" in req.text:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif "true" in req.text:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def office365(email):
    user_agent = 'Microsoft Office/16.0 (Windows NT 10.0; Microsoft Outlook 16.0.12026; Pro)'
    headers = {'User-Agent': user_agent, 'Accept': 'application/json'}
    r = requests.get('https://outlook.office365.com/autodiscover/autodiscover.json/v1.0/{}?Protocol=Autodiscoverv1'.format(email), headers=headers, allow_redirects=False)
    if r.status_code == 200:
         return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def live(email):
    ua = UserAgent()
    session= requests.session()
    session.headers={
        'User-Agent': ua.firefox,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://account.live.com/ResetPassword.aspx',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://account.live.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    req = session.get('https://account.live.com/password/reset')
    uaid=req.text.split('"clientTelemetry":{"uaid":"')[1].split('"')[0]
    amtcxt=req.text.split('<input type="hidden" id="amtcxt" name="amtcxt" value="')[1].split('"')[0]
    canary=req.text.split('<input type="hidden" id="canary" name="canary" value="')[1].split('"')[0]
    params = (
        ('uaid', uaid),
    )

    data = {
      'iAction': 'SignInName',
      'iRU': 'https://account.live.com/SummaryPage.aspx',
      'amtcxt': amtcxt,
      'uaid': uaid,
      'network_type': '',
      'isSigninNamePhone': 'False',
      'canary': canary,
      'PhoneCountry': '',
      'iSigninName': email
    }

    response = session.post('https://account.live.com/password/reset', params=params, data=data)
    if response.status_code==200:
        if int(str(len(response.text))[:2])<15:
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
