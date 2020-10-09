import requests,re,mechanize,json,random,string,queue,time
from bs4 import BeautifulSoup
from mechanize import Browser
try:
    import cookielib
except:
    import http.cookiejar as cookielib

from tqdm import tqdm
import argparse
from termcolor import colored
from threading import Thread
from holehe.localuseragent import *

def adobe(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
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
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
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

def buymeacoffe(email):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.buymeacoffee.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req=requests.get("https://www.buymeacoffee.com/",headers=headers)
    if req.status_code==200:
        csrf_token=req.text.split('<input type="hidden" id="csrf" name="bmc_csrf_token" value="')[1].split('"')[0]
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})


    cookies = {
        'bmccsrftoken': csrf_token,
    }


    data = {
      'email': email,
      'password': get_random_string(20),
      'bmc_csrf_token': csrf_token
    }

    response = requests.post('https://www.buymeacoffee.com/auth/validate_email_and_password', headers=headers, cookies=cookies, data=data)
    if response.status_code==200:
        data=response.json()
        if data["status"]=="SUCCESS":
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        elif data["status"]=="FAIL" and "email" in str(data):
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})


def ebay(email):

    s = requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        srt=s.get("https://www.ebay.com/signin/").text.split('"csrfAjaxToken":"')[1].split('"')[0]
    except IndexError as e:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

    data = {
      'identifier': email,
      'srt': srt
    }

    response = s.post('https://signin.ebay.com/signin/srv/identifer', data=data).json()
    if "err" in response.keys():
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
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
    try:
        profile_picture = soup.find('img', attrs={'class': 'img'}).get("src")
    except:
        profile_picture=""
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
    s = requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    freq=s.get("https://www.instagram.com/accounts/emailsignup/")
    token= freq.text.split('{"config":{"csrf_token":"')[1].split('"')[0]
    data = {
      'email': email,
      'username': '',
      'first_name': '',
      'opt_into_one_tap': 'false'
    }

    check = s.post("https://www.instagram.com/accounts/web_create_ajax/attempt/",data=data,headers={"x-csrftoken": token}).json()
    if 'email' in check["errors"].keys():
        if check["errors"]["email"][0]["code"]=="email_is_taken":
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        elif "email_sharing_limit" in str(check["errors"]):
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def tumblr(email):

    s = requests.session()

    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
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
def github(email):
    s = requests.session()
    freq = s.get("https://github.com/join")
    token_regex = re.compile(r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"')
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
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
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
    try:
        brows = Browser()
        brows.set_handle_robots(False)
        brows._factory.is_html = True
        brows.set_cookiejar(cookielib.LWPCookieJar())
        brows.addheaders = [('User-agent',random.choice(ua["browsers"]["firefox"]))]
        brows.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
        url = "https://account.live.com/password/reset"
        brows.open(url, timeout=10)
        brows.select_form(nr=0)
        brows.form['iSigninName'] = email
        brows.method = "POST"
        submit = brows.submit()
        data = json.loads(str('{"name":"'+str(submit.read().decode("utf-8")).split('"},{"name":"')[1].split('],"showExpirationCheckbox')[0]))
        if data["type"]=="Email":
            return({"rateLimit":False,"exists":True,"emailrecovery":data["name"],"phoneNumber":None,"others":None})
        elif data["type"]=="Sms":
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":data["name"],"others":None})
    except:
        pass

    session= requests.session()
    session.headers={
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
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
def evernote(email):

    ses = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.evernote.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.evernote.com/Login.action',
        'TE': 'Trailers',
    }
    ses.headers=headers
    data = ses.get("https://www.evernote.com/Login.action")
    data = {
      'username': email,
      'evaluateUsername': '',
      'hpts': data.text.split('document.getElementById("hpts").value = "')[1].split('"')[0],
      'hptsh': data.text.split('document.getElementById("hptsh").value = "')[1].split('"')[0],
      'analyticsLoginOrigin': 'login_action',
      'clipperFlow': 'false',
      'showSwitchService': 'true',
      'usernameImmutable': 'false',
      '_sourcePage': data.text.split('<input type="hidden" name="_sourcePage" value="')[1].split('"')[0],
      '__fp': data.text.split('<input type="hidden" name="__fp" value="')[1].split('"')[0]
    }
    response = ses.post('https://www.evernote.com/Login.action', data=data)
    if "usePasswordAuth" in response.text:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif "displayMessage" in response.text:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def amazon(email):
    brows = Browser()
    brows.set_handle_robots(False)
    brows._factory.is_html = True
    brows.set_cookiejar(cookielib.LWPCookieJar())
    brows.addheaders = [('User-agent',random.choice(ua["browsers"]["chrome"]))]
    brows.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
    url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    brows.open(url, timeout=10)
    brows.select_form(nr=0)
    brows.form['email'] = email

    brows.method = "POST"
    submit = brows.submit()
    soup = BeautifulSoup(submit.read().decode("utf-8"),"lxml")
    if soup.find("div", {"id": "auth-password-missing-alert"}):
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
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

    response = requests.get('https://lastpass.com/create_account.php', params=params,headers=headers)
    if response.text=="no":
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    if response.text=="ok" or response.text=="emailinvalid":
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def aboutme(email):

    s = requests.session()
    reqToken = s.get("https://about.me/signup",headers={'User-Agent': random.choice(ua["browsers"]["firefox"])}).text.split(',"AUTH_TOKEN":"')[1].split('"')[0]

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Auth-Token': reqToken,
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://about.me',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"user_name":"","first_name":"","last_name":"","allowed_features":[],"counters":{"id":"counters"},"settings":{"id":"settings","compliments":{"id":"compliments"},"follow":{"id":"follow"},"share":{"id":"share"}},"email_address":"'+email+'","honeypot":"","actions":{"id":"actions"},"apps":[],"contact":{"id":"contact"},"contact_me":{"id":"contact_me"},"email_channels":{"id":"email_channels"},"flags":{"id":"flags"},"images":[],"interests":[],"jobs":[],"layout":{"version":1,"id":"layout","color":"305B90"},"links":[],"locations":[],"mapped_domains":[],"portfolio":[],"roles":[],"schools":[],"slack_teams":[],"spotlight":{"type":null,"text":null,"url":null,"id":"spotlight"},"spotlight_trial":{"type":null,"text":null,"url":null,"id":"spotlight_trial"},"store":{"id":"store","credit_card":{"number":"","exp_month":"","exp_year":"","cvc":"","address_zip":"","last4":"","id":"credit_card"},"charges":[],"purchases":[]},"tags":[],"testimonials":{"header":"0","id":"testimonials","items":[]},"video":{"id":"video"},"signup":{"id":"signup","step":"email","method":"email"}}'

    response = s.post('https://about.me/n/signup', headers=headers, data=data)
    if response.status_code==409:
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif response.status_code==200:
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def discord(email):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"fingerprint":"","email":"'+email+'","username":"'+get_random_string(20)+'","password":"'+get_random_string(20)+'","invite":null,"consent":true,"date_of_birth":"","gift_code_sku_id":null,"captcha_key":null}'

    response = requests.post('https://discord.com/api/v8/auth/register', headers=headers, data=data)
    responseData=response.json()
    try:
        if "code" in responseData.keys():
            if str(responseData["code"])=="50035":
                try:
                    if responseData["errors"]["email"]["_errors"][0]['code']=="EMAIL_ALREADY_REGISTERED":
                        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
                except:
                    return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        elif responseData["captcha_key"][0]=="captcha-required":
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    except:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def yahoo(email):
    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://login.yahoo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    req = s.get("https://login.yahoo.com",headers=headers)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'bucket': 'mbr-fe-merge-manage-account',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://login.yahoo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = (
        ('.src', 'fpctx'),
        ('.intl', 'ca'),
        ('.lang', 'en-CA'),
        ('.done', 'https://ca.yahoo.com'),
    )
    try:
        data = {
          'acrumb': req.text.split('<input type="hidden" name="acrumb" value="')[1].split('"')[0],
          'sessionIndex': req.text.split('<input type="hidden" name="sessionIndex" value="')[1].split('"')[0],
          'username': email,
          'passwd': '',
          'signin': 'Next',
          'persistent': 'y'
        }

        response = s.post('https://login.yahoo.com/', headers=headers, params=params, data=data)
        response=response.json()
        if "error" in response.keys():
            if response["error"]==False:
                return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
            else:
                return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        elif "render" in response.keys():
            if response["render"]["error"]=="messages.ERROR_INVALID_USERNAME":
                return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
            else:
                return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    except:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def vrbo(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'x-homeaway-site': 'vrbo',
        'Origin': 'https://www.vrbo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"emailAddress":"'+email+'"}'

    response = requests.post('https://www.vrbo.com/auth/aam/v3/status', headers=headers, data=data)
    response=response.json()

    if "authType" in response.keys():
        if response["authType"][0]=="LOGIN_UMS":
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        elif response["authType"][0]=="SIGNUP":
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def samsung(email):
    req = requests.get("https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp")
    token =req.text.split("sJSESSIONID")[1].split('"')[1].split('"')[0]

    crsf=req.text.split("{'token' : '")[1].split("'")[0]

    cookies = {
        'EUAWSIAMSESSIONID': token,
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-CSRF-TOKEN': crsf,
        'Origin': 'https://account.samsung.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = (
        ('v', '1337'),
    )

    data = '{"emailID":"'+email+'"}'

    response = requests.post('https://account.samsung.com/accounts/v1/Samsung_com_FR/signUpCheckEmailIDProc', headers=headers, params=params, cookies=cookies, data=data)
    data=response.json()
    if response.status_code==200:
        if "rtnCd" in data.keys():
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def snapchat(email):
    req = requests.get("https://accounts.snapchat.com")
    xsrf=req.text.split('data-xsrf="')[1].split('"')[0]
    webClientId=req.text.split('ata-web-client-id="')[1].split('"')[0]
    url = "https://accounts.snapchat.com/accounts/merlin/login"
    headers = {
        "Host": "accounts.snapchat.com",
        "User-Agent": random.choice(ua["browsers"]["firefox"]),
        "Accept": "*/*",
        "X-XSRF-TOKEN": xsrf,
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Content-Length": "51",
        "Connection": "close",
        "Cookie": "xsrf_token="+xsrf+"; web_client_id="+webClientId
    }
    data = '{"email":'+email+',"app":"BITMOJI_APP"}'

    response = requests.post(url, data=data, headers=headers)
    if response.status_code!=204:
        data=response.json()
        return({"rateLimit":False,"exists":data["hasSnapchat"],"emailrecovery":None,"phoneNumber":None,"others":None})
    return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def bitmoji(email):
    req = requests.get("https://accounts.snapchat.com")
    xsrf=req.text.split('data-xsrf="')[1].split('"')[0]
    webClientId=req.text.split('ata-web-client-id="')[1].split('"')[0]
    url = "https://accounts.snapchat.com/accounts/merlin/login"
    headers = {
        "Host": "accounts.snapchat.com",
        "User-Agent": random.choice(ua["browsers"]["firefox"]),
        "Accept": "*/*",
        "X-XSRF-TOKEN": xsrf,
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Content-Length": "51",
        "Connection": "close",
        "Cookie": "xsrf_token="+xsrf+"; web_client_id="+webClientId
    }
    data = '{"email":'+email+',"app":"BITMOJI_APP"}'

    response = requests.post(url, data=data, headers=headers)
    if response.status_code!=204:
        data=response.json()
        return({"rateLimit":False,"exists":data["hasBitmoji"],"emailrecovery":None,"phoneNumber":None,"others":None})
    return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def blablacar(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'fr_FR',
        'Referer': 'https://www.blablacar.fr/',
        'Content-Type': 'application/json',
        'x-locale': 'fr_FR',
        'x-currency': 'EUR',
        'x-client': 'SPA|1.0.0',
        'x-forwarded-proto': 'https',
        'Origin': 'https://www.blablacar.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        appToken=requests.get("https://www.blablacar.fr/register",headers=headers).text.split(',"appToken":"')[1].split('"')[0]
    except:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

    cookies = {
        'datadome': 'eee',
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'fr_FR',
        'Referer': 'https://www.blablacar.fr/',
        'Content-Type': 'application/json',
        'x-locale': 'fr_FR',
        'x-currency': 'EUR',
        'x-client': 'SPA|1.0.0',
        'x-forwarded-proto': 'https',
        'Authorization': 'Bearer '+appToken,
        'Origin': 'https://www.blablacar.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    response = requests.get('https://edge.blablacar.fr/auth/validation/email/'+email, headers=headers, cookies=cookies)
    data=response.json()
    if "url" in data.keys():
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif "exists" in data.keys():
        return({"rateLimit":False,"exists":data["exists"],"emailrecovery":None,"phoneNumber":None,"others":None})

def freelancer(email):
    s=requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/json',
        'Origin': 'https://www.freelancer.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = (
        ('compact', 'true'),
        ('new_errors', 'true'),
    )

    data = '{"user":{"email":"'+email+'"}}'
    response = s.post('https://www.freelancer.com/api/users/0.1/users/check', params=params, data=data)
    resData=response.json()
    if response.status_code==409:
        if "EMAIL_ALREADY_IN_USE" in response.text:
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})

    elif response.status_code==200:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def google(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Same-Domain': '1',
        'Google-Accounts-XSRF': '1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }


    req = requests.get("https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp",headers=headers)
    try:
        freq=req.text.split('quot;,null,null,null,&quot;')[1].split('&quot')[0]
    except:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

    params = (
        ('hl', 'fr'),
        ('rt', 'j'),
    )

    data = {
      'continue': 'https://www.google.com/',
      'dsh': '',
      'hl': 'fr',
      'f.req': '["'+freq+'","","","'+email+'",false]',
      'azt': '',
      'cookiesDisabled': 'false',
      'deviceinfo': '[null,null,null,[],null,null,null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,null,0,null,false]',
      'gmscoreversion': 'undefined',
      '': ''
    }
    response = requests.post('https://accounts.google.com/_/signup/webusernameavailability', headers=headers, params=params, data=data)
    if '"gf.wuar",2' in response.text:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif '"gf.wuar",1' in response.text or "EmailInvalid" in response.text:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
def nike(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://www.nike.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nike.com/',
        'TE': 'Trailers',
    }

    params = (
        ('appVersion', '831'),
        ('experienceVersion', '831'),
        ('uxid', 'com.nike.commerce.nikedotcom.web'),
        ('locale', 'fr_FR'),
        ('backendEnvironment', 'identity'),
        ('browser', ''),
        ('mobile', 'false'),
        ('native', 'false'),
        ('visit', '1'),
    )

    data = '{"emailAddress":"'+email+'"}'

    response = requests.post('https://unite.nike.com/account/email/v1', headers=headers, params=params, data=data)
    if response.status_code==409:
        return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif response.status_code==204:
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})


def wordpress(email):
    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ccpa_applies': 'true',
        'usprivacy': '1YNN',
        'landingpage_currency': 'EUR',
        'wordpress_test_cookie': 'WP+Cookie+check',
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = (
        ('http_envelope', '1'),
        ('locale', 'fr'),
    )

    response = requests.get('https://public-api.wordpress.com/rest/v1.1/users/'+email+'/auth-options', headers=headers, params=params, cookies=cookies)
    info =response.json()
    if "email_verified" in info["body"].keys():
        if info["body"]["email_verified"]==True:
            return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
        else:
            return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    elif "unknown_user" in str(info) or "email_login_not_allowed" in str(info):
        return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

def eventbrite(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.eventbrite.com/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.eventbrite.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    req = requests.get("https://www.eventbrite.com/signin/?referrer=%2F",headers=headers)
    try:
        csrf_token=req.cookies["csrftoken"]

    except:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})

    cookies = {
        'csrftoken': csrf_token,
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.eventbrite.com/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token,
        'Origin': 'https://www.eventbrite.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"email":"'+email+'"}'

    response = requests.post('https://www.eventbrite.com/api/v3/users/lookup/', headers=headers, cookies=cookies, data=data)
    if response.status_code==200:
        try:
            reqd=response.json()
            if reqd["exists"]==True:
                return({"rateLimit":False,"exists":True,"emailrecovery":None,"phoneNumber":None,"others":None})
            else:
                return({"rateLimit":False,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
        except:
            return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})
    else:
        return({"rateLimit":True,"exists":False,"emailrecovery":None,"phoneNumber":None,"others":None})




def main():
    print('Github : https://github.com/megadose/holehe')
    start_time = time.time()
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    parser.add_argument("-e", "--email", help="Email of the target",required=True)
    args = parser.parse_args()

    def websiteName(WebsiteFunction,Websitename,email):
        return({Websitename:WebsiteFunction(email)})

    websites=[eventbrite,nike,google,wordpress,freelancer,blablacar,buymeacoffe,snapchat,bitmoji,samsung,aboutme,adobe,amazon,discord,ebay,evernote,facebook,firefox,github,instagram,lastfm,lastpass,live,office365,pinterest,spotify,tumblr,twitter,vrbo,yahoo]

    que = queue.Queue()
    infos ={}
    threads_list = []

    for website in websites:
        t = Thread(target=lambda q, arg1: q.put(websiteName(website,website.__name__,args.email)), args=(que, website))
        t.start()
        threads_list.append(t)

    for t in tqdm(threads_list):
        t.join()


    while not que.empty():
        result = que.get()
        key, value = next(iter(result.items()))
        infos[key]=value

    description = colored("Email used","green")+","+colored(" Email not used","magenta")+","+colored(" Rate limit","red")
    print("\033[H\033[J")
    print("*"*25)
    print(args.email)
    print("*"*25)
    for i in sorted(infos):
        key, value = i,infos[i]
        i = value
        if i["rateLimit"]==True:
            websiteprint=colored(key,"red")
        elif i["exists"]==False :
            websiteprint=colored(key,"magenta")
        else:
            toprint=""
            if i["emailrecovery"]!= None:
                toprint+=" "+i["emailrecovery"]
            if i["phoneNumber"]!= None:
                toprint+=" / "+i["phoneNumber"]
            if i["others"]!= None:
                toprint+=" / FullName "+i["others"]["FullName"]

            websiteprint=colored(str(key)+toprint,"green")
        print(websiteprint)

    print("\n"+description)
    print(str(len(websites))+" websites checked in "+str(round(time.time() - start_time,2))+ " seconds")
