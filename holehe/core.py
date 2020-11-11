import hashlib
import requests
import re
import mechanize
import json
import random
import string
import queue
import time
import argparse
from tqdm import tqdm
from termcolor import colored
from threading import Thread
from bs4 import BeautifulSoup
from mechanize import Browser
try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib
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

    data = '{"username":"' + email + '","accountType":"individual"}'
    r = requests.post(
        'https://auth.services.adobe.com/signin/v1/authenticationstate',
        headers=headers,
        data=data).json()
    if "errorCode" in str(r.keys()):
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-IMS-Authentication-State'] = r['id']
    params = (
        ('purpose', 'passwordRecovery'),
    )
    response = requests.get(
        'https://auth.services.adobe.com/signin/v2/challenges',
        headers=headers,
        params=params).json()
    return({"rateLimit": False, "exists": True, "emailrecovery": response['secondaryEmail'], "phoneNumber": response['securityPhoneNumber'], "others": None})
def anydo(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://desktop.any.do/',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Platform': '3',
        'Origin': 'https://desktop.any.do',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"email":"'+email+'"}'

    response = requests.post('https://sm-prod2.any.do/check_email', headers=headers, data=data)
    if response.status_code==200:
        if response.json()["user_exists"]==True:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def pornhub(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    s = requests.session()
    req = s.get("https://www.pornhub.com/signup", headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    try:
        toe = soup.find(attrs={"name": "token"}).get("value")
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    params = (
        ('token', toe),
    )

    data = {
        'check_what': 'email',
        'email': email
    }

    response = s.post(
        'https://www.pornhub.com/user/create_account_check',
        headers=headers,
        params=params,
        data=data)
    try:
        if response.json()["error_message"] == "Email has been taken.":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def sevencups(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]), 'DNT': '1',
        'Connection': 'keep-alive', 'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'www.7cups.com', 'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.7cups.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.7cups.com/listener/CreateAccount.php', 'TE': 'Trailers',
        'Content-Type': 'multipart/form-data; boundary=---------------------------'

    }

    data = '-----------------------------\r\nContent-Disposition: form-data; name="email"\r\n\r\n' + email + '\r\n-----------------------------\r\nContent-Disposition: form-data; name="passwd"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobMonth"\r\n\r\n12\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobDay"\r\n\r\n11\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobYear"\r\n\r\n2010\r\n-----------------------------\r\nContent-Disposition: form-data; name="orgPass"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name="data-request-datatype"\r\n\r\njson\r\n-----------------------------\r\nContent-Disposition: form-data; name="submit-value"\r\n\r\nnull\r\n-------------------------------\r\n'

    response = requests.post(
        'https://www.7cups.com/listener/CreateAccount.php',
        data=data,
        headers=headers)
    if response.status_code == 200:
        if "Account already exists with this email address" in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
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


def codepen(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://codepen.io/accounts/signup/user/free',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://codepen.io',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        s = requests.session()
        req = s.get(
            "https://codepen.io/accounts/signup/user/free",
            headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")
        token = soup.find(attrs={"name": "csrf-token"}).get("content")
        headers["X-CSRF-Token"] = token
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = {
        'attribute': 'email',
        'value': email,
        'context': 'user'
    }

    response = s.post(
        'https://codepen.io/accounts/duplicate_check',
        headers=headers,
        data=data)
    if "That Email is already taken." in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def taringa(email):
    cookies = {
        'G_ENABLED_IDPS': 'google',
    }

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://www.taringa.net',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"email":"'+email+'"}'

    response = requests.post('https://www.taringa.net/api/auth/availability/email', headers=headers, cookies=cookies, data=data)
    if response.status_code==200:
        if '{"available":false}' == response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.status_code==400:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def voxmedia(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://auth.voxmedia.com/login',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://auth.voxmedia.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {
      'email': email
    }

    response = requests.post('https://auth.voxmedia.com/chorus_auth/email_valid.json', headers=headers, data=data)
    try:
        rep=response.json()
        if rep["available"]==True:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    except :
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})



def buymeacoffe(email):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.buymeacoffee.com',
        'DNT': '1',
        'TE': 'Trailers',
    }
    r = requests.get("https://www.buymeacoffee.com/", headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(req.content, features="lxml")
        csrf_token = soup.find(attrs={'name': 'bmc_csrf_token'}).get("value")
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'bmccsrftoken': csrf_token,
    }
    data = {
        'email': email,
        'password': get_random_string(20),
        'bmc_csrf_token': csrf_token
    }

    r = requests.post(
        'https://www.buymeacoffee.com/auth/validate_email_and_password',
        headers=headers,
        cookies=cookies,
        data=data)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "SUCCESS":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif data["status"] == "FAIL" and "email" in str(data):
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def codecademy(email):
    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.codecademy.com/register?redirect=%2',
        'Content-Type': 'application/json',
        'Origin': 'https://www.codecademy.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req = s.get(
        "https://www.codecademy.com/register?redirect=%2F",
        headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    try:
        headers["X-CSRF-Token"] = soup.find(
            attrs={"name": "csrf-token"}).get("content")
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = '{"user":{"email":"' + email + '"}}'

    response = s.post(
        'https://www.codecademy.com/register/validate',
        headers=headers,
        data=data)
    if 'is already taken' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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
        srt = s.get(
            "https://www.ebay.com/signin/").text.split('"csrfAjaxToken":"')[1].split('"')[0]
    except IndexError as e:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = {
        'identifier': email,
        'srt': srt
    }

    response = s.post(
        'https://signin.ebay.com/signin/srv/identifer',
        data=data).json()
    if "err" in response.keys():
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})


def facebook(email):
    s = requests.Session()
    req = s.get('https://www.facebook.com/login/identify?ctx=recover&lwv=110')
    token = re.findall(r'"token":"([a-zA-Z0-9_-]+)"', req.text)[0]
    if not token:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": {"FullName": None, "profilePicture": None}})

    pattern = r'"_js_datr","([a-zA-Z0-9_-]+)"'
    jsdatr = re.findall(pattern, req.text)[0]
    if not jsdatr:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": {"FullName": None, "profilePicture": None}})

    data = {'lsd': token,
            'email': email,
            'did_submit': 'Search',
            '__user': 0,
            '__a': 1}
    cookies = {'_js_datr': jsdatr + ';'}
    headers = {
        'referer': 'https://www.facebook.com/login/identify?ctx=recover&lwv=110'}
    req = s.post(
        'https://www.facebook.com/ajax/login/help/identify.php?ctx=recover',
        cookies=cookies,
        data=data,
        headers=headers)

    pattern = r'ldata=([a-zA-Z0-9-_]+)\\"'
    try:
        ldata = re.findall(pattern, req.text)[0]
    except IndexError:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": {"FullName": None, "profilePicture": None}})
    if not ldata:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": {"FullName": None, "profilePicture": None}})

    req = s.get('https://www.facebook.com/recover/initiate?ldata=%s' % ldata)
    soup = BeautifulSoup(req.content, features="lxml")
    full_name = soup.find('div', attrs={'class': 'fsl fwb fcb'})
    try:
        profile_picture = soup.find('img', attrs={'class': 'img'}).get('src')
    except BaseException:
        profile_picture = ""
    try:
        emailrecovery = req.text.split(
            '</strong><br /><div>')[1].split("</div>")[0].replace("&#064;", "@").replace('<div class="_2pic">', "")
        if emailrecovery == email:
            emailrecovery = None

    except IndexError:
        emailrecovery = None
    try:
        phone = req.text.split(
            '</strong><br /><div dir="ltr">+')[1].split("</div>")[0]
    except IndexError:
        phone = None
    if full_name is None:
        full_name = ""
    else:
        if full_name != email:
            full_name = full_name.text

    return({"rateLimit": False, "exists": True, "emailrecovery": emailrecovery, "phoneNumber": phone, "others": {"FullName": full_name, "profilePicture": profile_picture}})


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

    freq = s.get("https://www.instagram.com/accounts/emailsignup/")
    token = freq.text.split('{"config":{"csrf_token":"')[1].split('"')[0]
    data = {
        'email': email,
        'username': '',
        'first_name': '',
        'opt_into_one_tap': 'false'
    }

    check = s.post(
        "https://www.instagram.com/accounts/web_create_ajax/attempt/",
        data=data,
        headers={
            "x-csrftoken": token}).json()
    if 'email' in check["errors"].keys():
        if check["errors"]["email"][0]["code"] == "email_is_taken":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif "email_sharing_limit" in str(check["errors"]):
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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
    firstreq = s.get("https://www.tumblr.com/login")
    # print(firstreq.text)
    data = [
        ('determine_email', email),
        ('user[email]', ''),
        ('user[password]', ''),
        ('tumblelog[name]', ''),
        ('user[age]', ''),
        ('context', 'no_referer'),
        ('version', 'STANDARD'),
        ('follow', ''),
        ('form_key', firstreq.text.split(
            '<meta name="tumblr-form-key" id="tumblr_form_key" content="')[1].split('"')[0]),
        ('seen_suggestion', '0'),
        ('used_suggestion', '0'),
        ('used_auto_suggestion', '0'),
        ('about_tumblr_slide', ''),
        ('random_username_suggestions', firstreq.text.split(
            'id="random_username_suggestions" name="random_username_suggestions" value="')[1].split('"')[0]),
        ('action', 'signup_determine'),
        ('action', 'signup_determine'),
        ('tracking_url', '/login'),
        ('tracking_version', 'modal'),
    ]

    response = s.post('https://www.tumblr.com/svc/account/register', data=data)
    if response.text == '{"redirect":false,"redirect_method":"GET","errors":[],"signup_success":false,"next_view":"signup_magiclink"}':
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def github(email):
    s = requests.session()
    freq = s.get("https://github.com/join")
    token_regex = re.compile(
        r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"')
    token = re.findall(token_regex, freq.text)
    data = {"value": email, "authenticity_token": token[0]}
    # print(data)
    req = s.post("https://github.com/signup_check/email", data=data)
    if "Your browser did something unexpected." in req.text:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
    if req.status_code == 422:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    if req.status_code == 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})

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
    soup=BeautifulSoup(r.text,features="lxml")
    token=soup.find(attrs={"id":"token"}).get("value")
    if token==None:
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

def twitter(email):
    req = requests.get(
        "https://api.twitter.com/i/users/email_available.json",
        params={
            "email": email})
    if req.json()["taken"] == True:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def pinterest(email):
    req = requests.get(
        "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
        params={
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'})
    if req.json()["resource_response"]["data"]:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def lastfm(email):
    req = requests.get("https://www.last.fm/join")
    try:
        token = req.cookies["csrftoken"]
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = {"csrfmiddlewaretoken": token, "userName": "", "email": email}
    headers = {
        "Accept": "*/*",
        "Referer": "https://www.last.fm/join",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"csrftoken={token}",
    }
    check = requests.post(
        "https://www.last.fm/join/partial/validate",
        headers=headers,
        data=data).json()
    if check["email"]["valid"]:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})


def coroflot(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.coroflot.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.coroflot.com/signup',
        'TE': 'Trailers',
    }

    data = {
        'email': email
    }
    response = requests.post(
        'https://www.coroflot.com/home/signup_email_check',
        headers=headers,
        data=data)
    try:
        if response.json()["data"] == -2:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    req = requests.get(
        'https://spclient.wg.spotify.com/signup/public/v1/account',
        headers=headers,
        params=params)
    if req.json()["status"] == 1:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif req.json()["status"] == 20:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})


def firefox(email):
    req = requests.post(
        "https://api.accounts.firefox.com/v1/account/status",
        data={
            "email": email})
    if "false" in req.text:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "true" in req.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def office365(email):
    user_agent = 'Microsoft Office/16.0 (Windows NT 10.0; Microsoft Outlook 16.0.12026; Pro)'
    headers = {'User-Agent': user_agent, 'Accept': 'application/json'}
    r = requests.get(
        'https://outlook.office365.com/autodiscover/autodiscover.json/v1.0/{}?Protocol=Autodiscoverv1'.format(
            email),
        headers=headers,
        allow_redirects=False)
    if r.status_code == 200:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def live(email):
    brows = Browser()
    brows.set_handle_robots(False)
    brows._factory.is_html = True
    brows.set_cookiejar(cookielib.LWPCookieJar())
    brows.addheaders = [
        ('User-agent',
         random.choice(
             ua["browsers"]["firefox"]))]
    brows.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(), max_time=1)
    url = "https://account.live.com/password/reset"
    brows.open(url, timeout=10)
    brows.select_form(nr=0)
    brows.form['iSigninName'] = email
    brows.method = "POST"
    submit = brows.submit()
    try:
        datatext=str('{"name":"' + str(submit.read().decode("utf-8")).split('"},{"name":"')[1].split('],"showExpirationCheckbox')[0])
    except IndexError:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    if "},{" in datatext:
        data1=json.loads(datatext.split("},{")[0]+"}")
        data2=json.loads("{"+datatext.split("},{")[1])
        if "@" in data1["name"]:
            return({"rateLimit": False, "exists": True, "emailrecovery": data1["name"], "phoneNumber": data2["name"], "others": None})
        elif "@" in data2["name"]:
            return({"rateLimit": False, "exists": True, "emailrecovery": data2["name"], "phoneNumber": data1["name"], "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data1["name"], "others": None})
    data = json.loads(datatext)
    if data["type"] == "Email":
        return({"rateLimit": False, "exists": True, "emailrecovery": data["name"], "phoneNumber": None, "others": None})
    elif data["type"] == "Sms":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data["name"], "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data2["name"], "others": None})


def rambler(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://id.rambler.ru/champ/registration',
        'Content-Type': 'application/json',
        'Origin': 'https://id.rambler.ru',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"method":"Rambler::Id::get_email_account_info","params":[{"email":"' + email + '"}],"rpc":"2.0"}'

    response = requests.post(
        'https://id.rambler.ru/jsonrpc',
        headers=headers,
        data=data)
    try:
        if response.json()["result"]["exists"] == 0:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def teamtreehouse(email):
    s = requests.Session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://teamtreehouse.com/subscribe/new?trial=yes',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://teamtreehouse.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    req = s.get(
        "https://teamtreehouse.com/subscribe/new?trial=yes",
        headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    token = soup.find(attrs={"name": "csrf-token"}).get("content")
    headers['X-CSRF-Token'] = token

    data = {
        'email': email
    }

    response = s.post(
        'https://teamtreehouse.com/account/email_address',
        headers=headers,
        data=data)
    if 'that email address is taken.' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text == '{"success":true}':
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def evernote(email):

    s = requests.session()
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
    s.headers = headers
    data = s.get("https://www.evernote.com/Login.action")
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
    response = s.post('https://www.evernote.com/Login.action', data=data)
    if "usePasswordAuth" in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "displayMessage" in response.text:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def amazon(email):
    brows = Browser()
    brows.set_handle_robots(False)
    brows._factory.is_html = True
    brows.set_cookiejar(cookielib.LWPCookieJar())
    brows.addheaders = [
        ('User-agent',
         random.choice(
             ua["browsers"]["chrome"]))]
    brows.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(),
        max_time=1)
    url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    brows.open(url, timeout=10)
    brows.select_form(nr=0)
    brows.form['email'] = email

    brows.method = "POST"
    submit = brows.submit()
    soup = BeautifulSoup(submit.read().decode("utf-8"), "lxml")
    if soup.find("div", {"id": "auth-password-missing-alert"}):
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    response = requests.get(
        'https://lastpass.com/create_account.php',
        params=params,
        headers=headers)
    if response.text == "no":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    if response.text == "ok" or response.text == "emailinvalid":
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def myspace(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://myspace.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://myspace.com/signup/email',
    }

    s=requests.session()

    r=s.get("https://myspace.com/signup/email",headers=headers,timeout=3)

    headers['Content-Type']= 'application/x-www-form-urlencoded; charset=UTF-8'
    try:
        headers['Hash']= r.text.split('<input name="csrf" type="hidden" value="')[1].split('"')[0]
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'

    data = {
      'email': email
    }

    response = requests.post('https://myspace.com/ajax/account/validateemail', headers=headers, data=data,timeout=3)
    try:
        if "This email address was already used to create an account." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def aboutme(email):

    s = requests.session()
    reqToken = s.get("https://about.me/signup", headers={'User-Agent': random.choice(
        ua["browsers"]["firefox"])}).text.split(',"AUTH_TOKEN":"')[1].split('"')[0]

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

    data = '{"user_name":"","first_name":"","last_name":"","allowed_features":[],"counters":{"id":"counters"},"settings":{"id":"settings","compliments":{"id":"compliments"},"follow":{"id":"follow"},"share":{"id":"share"}},"email_address":"' + email + \
        '","honeypot":"","actions":{"id":"actions"},"apps":[],"contact":{"id":"contact"},"contact_me":{"id":"contact_me"},"email_channels":{"id":"email_channels"},"flags":{"id":"flags"},"images":[],"interests":[],"jobs":[],"layout":{"version":1,"id":"layout","color":"305B90"},"links":[],"locations":[],"mapped_domains":[],"portfolio":[],"roles":[],"schools":[],"slack_teams":[],"spotlight":{"type":null,"text":null,"url":null,"id":"spotlight"},"spotlight_trial":{"type":null,"text":null,"url":null,"id":"spotlight_trial"},"store":{"id":"store","credit_card":{"number":"","exp_month":"","exp_year":"","cvc":"","address_zip":"","last4":"","id":"credit_card"},"charges":[],"purchases":[]},"tags":[],"testimonials":{"header":"0","id":"testimonials","items":[]},"video":{"id":"video"},"signup":{"id":"signup","step":"email","method":"email"}}'

    response = s.post('https://about.me/n/signup', headers=headers, data=data)
    if response.status_code == 409:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.status_code == 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def strava(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    s=requests.session()
    r=s.get("https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show",headers=headers)
    try:
        headers['X-CSRF-Token']= r.text.split('<meta name="csrf-token" content="')[1].split('"')[0]
    except:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = s.get('https://www.strava.com/athletes/email_unique', headers=headers, params=params)

    if response.text=="false":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text=="true":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})



def demonforums(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://demonforums.net/member.php',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://demonforums.net',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r=s.get("https://demonforums.net/member.php",headers=headers)
    if "Your request was blocked" in r.text or r.status_code!=200:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'


    params = (
        ('action', 'email_availability'),
    )
    try:
        data = {
          'email': email,
          'my_post_key':r.text.split('var my_post_key = "')[1].split('"')[0]
        }
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    response = s.post('https://demonforums.net/xmlhttp.php', headers=headers, params=params, data=data)
    if "Your request was blocked" not in response.text and response.status_code==200:
        if "email address that is already in use by another member." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

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

    data = '{"fingerprint":"","email":"' + email + '","username":"' + get_random_string(20) + '","password":"' + get_random_string(
        20) + '","invite":null,"consent":true,"date_of_birth":"","gift_code_sku_id":null,"captcha_key":null}'

    response = requests.post(
        'https://discord.com/api/v8/auth/register',
        headers=headers,
        data=data)
    responseData = response.json()
    try:
        if "code" in responseData.keys():
            try:
                if responseData["errors"]["email"]["_errors"][0]['code'] == "EMAIL_ALREADY_REGISTERED":
                    return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
                else:
                    return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            except BaseException:
                return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif responseData["captcha_key"][0] == "captcha-required":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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
    req = s.get("https://login.yahoo.com", headers=headers)

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

        response = s.post(
            'https://login.yahoo.com/',
            headers=headers,
            params=params,
            data=data)
        response = response.json()
        if "error" in response.keys():
            if response["error"] == False:
                return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif "render" in response.keys():
            if response["render"]["error"] == "messages.ERROR_INVALID_USERNAME":
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    data = '{"emailAddress":"' + email + '"}'

    response = requests.post(
        'https://www.vrbo.com/auth/aam/v3/status',
        headers=headers,
        data=data)
    response = response.json()

    if "authType" in response.keys():
        if response["authType"][0] == "LOGIN_UMS":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif response["authType"][0] == "SIGNUP":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def samsung(email):
    req = requests.get(
        "https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp")
    token = req.text.split("sJSESSIONID")[1].split('"')[1].split('"')[0]

    crsf = req.text.split("{'token' : '")[1].split("'")[0]

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

    data = '{"emailID":"' + email + '"}'

    response = requests.post(
        'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUpCheckEmailIDProc',
        headers=headers,
        params=params,
        cookies=cookies,
        data=data)
    data = response.json()
    if response.status_code == 200:
        if "rtnCd" in data.keys():
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def snapchat(email):
    req = requests.get("https://accounts.snapchat.com")
    xsrf = req.text.split('data-xsrf="')[1].split('"')[0]
    webClientId = req.text.split('ata-web-client-id="')[1].split('"')[0]
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
        "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
    }
    data = '{"email":' + email + ',"app":"BITMOJI_APP"}'

    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 204:
        data = response.json()
        return({"rateLimit": False, "exists": data["hasSnapchat"], "emailrecovery": None, "phoneNumber": None, "others": None})
    return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def bitmoji(email):
    req = requests.get("https://accounts.snapchat.com")
    xsrf = req.text.split('data-xsrf="')[1].split('"')[0]
    webClientId = req.text.split('ata-web-client-id="')[1].split('"')[0]
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
        "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
    }
    data = '{"email":' + email + ',"app":"BITMOJI_APP"}'

    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 204:
        data = response.json()
        return({"rateLimit": False, "exists": data["hasBitmoji"], "emailrecovery": None, "phoneNumber": None, "others": None})
    return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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
        appToken = requests.get(
            "https://www.blablacar.fr/register",
            headers=headers).text.split(',"appToken":"')[1].split('"')[0]
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'datadome': '',
    }

    headers["Authorization"] = 'Bearer ' + appToken

    response = requests.get(
        'https://edge.blablacar.fr/auth/validation/email/' +
        email,
        headers=headers,
        cookies=cookies)
    data = response.json()
    if "url" in data.keys():
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "exists" in data.keys():
        return({"rateLimit": False, "exists": data["exists"], "emailrecovery": None, "phoneNumber": None, "others": None})


def freelancer(email):
    s = requests.session()
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

    data = '{"user":{"email":"' + email + '"}}'
    response = s.post(
        'https://www.freelancer.com/api/users/0.1/users/check',
        params=params,
        data=data)
    resData = response.json()
    if response.status_code == 409:
        if "EMAIL_ALREADY_IN_USE" in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})

    elif response.status_code == 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def google(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Same-Domain': '1',
        'Google-Accounts-XSR': '1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    req = requests.get(
        "https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp",
        headers=headers)
    try:
        freq = req.text.split('quot;,null,null,null,&quot;')[
            1].split('&quot')[0]
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    params = (
        ('hl', 'fr'),
        ('rt', 'j'),
    )

    data = {
        'continue': 'https://www.google.com/',
        'dsh': '',
        'hl': 'fr',
        'f.req': '["' + freq + '","","","' + email + '",false]',
        'azt': '',
        'cookiesDisabled': 'false',
        'deviceinfo': '[null,null,null,[],null,null,null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,null,0,null,false]',
        'gmscoreversion': 'undefined',
        '': ''
    }
    response = requests.post(
        'https://accounts.google.com/_/signup/webusernameavailability',
        headers=headers,
        params=params,
        data=data)
    if '"gf.wuar",2' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif '"gf.wuar",1' in response.text or "EmailInvalid" in response.text:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    data = '{"emailAddress":"' + email + '"}'

    response = requests.post(
        'https://unite.nike.com/account/email/v1',
        headers=headers,
        params=params,
        data=data)
    if response.status_code == 409:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.status_code == 204:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    response = requests.get(
        'https://public-api.wordpress.com/rest/v1.1/users/' +
        email +
        '/auth-options',
        headers=headers,
        params=params,
        cookies=cookies)
    info = response.json()
    if "email_verified" in info["body"].keys():
        if info["body"]["email_verified"] == True:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "unknown_user" in str(info) or "email_login_not_allowed" in str(info):
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def ello(email):

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://ello.co/join',
        'Content-Type': 'application/json',
        'Origin': 'https://ello.co',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"email":"' + email + '"}'
    try:
        response = requests.post('https://ello.co/api/v2/availability',headers=headers,data=data)
        if response.json()["availability"]["email"] == True:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def issuu(email):

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://issuu.com/signup?returnUrl=https%3A%2F%2Fissuu.com%2F&issuu_product=header&issuu_subproduct=anon_home&issuu_context=signin&issuu_cta=log_up',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    response = requests.get(
        'https://issuu.com/call/signup/check-email/' +
        email,
        headers=headers)
    try:
        if response.json()["status"] == "unavailable":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def plurk(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.plurk.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = {
      'email': email
    }

    response = requests.post('https://www.plurk.com/Users/isEmailFound', headers=headers, data=data)
    if response.text=="True":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text=="False":
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})



def envato(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://themeforest.net/',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://themeforest.net',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {
        'email': email
    }
    response = requests.post(
        'https://account.envato.com/api/validate_email',
        headers=headers,
        data=data)
    if 'Email is already in use' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "Page designed by Kotulsky" in response.text:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


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

    req = requests.get(
        "https://www.eventbrite.com/signin/?referrer=%2F",
        headers=headers)
    try:
        csrf_token = req.cookies["csrftoken"]

    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'csrftoken': csrf_token,
    }

    headers["X-CSRFToken"] = csrf_token
    data = '{"email":"' + email + '"}'

    response = requests.post(
        'https://www.eventbrite.com/api/v3/users/lookup/',
        headers=headers,
        cookies=cookies,
        data=data)
    if response.status_code == 200:
        try:
            reqd = response.json()
            if reqd["exists"] == True:
                return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def venmo(email):
    s = requests.Session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://venmo.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://venmo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    s.get("https://venmo.com/signup/email",headers=headers)
    try:
        headers["device-id"]=s.cookies["v_id"]
    except :
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = '{"last_name":"e","first_name":"z","email":"'+email+'","password":"","phone":"1","client_id":10}'

    response = s.post('https://venmo.com/api/v5/users', headers=headers, data=data)
    if "Not acceptable" not in response.text:
        if "That email is already registered in our system." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def odnoklassniki(email):
    # credits: https://github.com/shllwrld/ok_checker/
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://ok.ru/',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    OK_LOGIN_URL = 'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
    OK_RECOVER_URL = 'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'

    session = requests.Session()
    session.headers.update(headers)
    session.get(OK_LOGIN_URL+'&st.email='+email)
    request = session.get(OK_RECOVER_URL)
    root_soup = BeautifulSoup(request.content, 'html.parser')
    soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
    if soup:
        account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
        masked_email = soup.find('button', {'data-l': 't,email'})
        masked_phone = soup.find('button', {'data-l': 't,phone'})
        if masked_phone:
            masked_phone = masked_phone.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if masked_email:
            masked_email = masked_email.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if account_info:
            masked_name = account_info.find('div', {'class': 'ext-registration_username_header'})
            if masked_name:
                masked_name = masked_name.get_text()
            account_info = account_info.findAll('div', {'class': 'lstp-t'})
            if account_info:
                profile_info = account_info[0].get_text()
                profile_registred = account_info[1].get_text()
            else:
                profile_info = None
                profile_registred = None
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

        others = {
            # TODO: split info separate fields, now only FullName displayed
            'FullName': '; '.join([masked_name, profile_info, profile_registred]),
        }

        return({"rateLimit": False, "exists": True, "emailrecovery": masked_email, "phoneNumber": masked_phone, "others": others})

    if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def mail_ru(email):
    headers = {
        'authority': 'account.mail.ru',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://account.mail.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://account.mail.ru/recovery?email={email}',
        'user-agent': random.choice(ua["browsers"]["chrome"]),
        'accept-language': 'ru',
    }

    data = 'email={email}&htmlencoded=false'.replace('@', '%40')

    response = requests.post(
        'https://account.mail.ru/api/v1/user/password/restore',
        headers=headers,
        data=data)

    if response.status_code == 200:
        try:
            reqd = response.json()
            if reqd['status'] == 200:
                phones = ', '.join(reqd['body'].get('phones', [])) or None
                emails = ', '.join(reqd['body'].get('emails', [])) or None
                return({"rateLimit": False, "exists": True, "emailrecovery": emails, "phoneNumber": phones, "others": None})
            else:
                # email not exists or some problem
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def xing(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    s = requests.session()
    response = s.get("https://www.xing.com/start/signup?registration=1", headers=headers)
    headers['x-csrf-token'] = response.cookies["xing_csrf_token"]

    data = {
      'signup_minireg': {
	'email': email,
	'password': '',
	'tandc_check': '1',
	'signup_channel': 'minireg_fullpage',
	'first_name': '',
	'last_name': ''
      }
    }

    response = s.post('https://www.xing.com/welcome/api/signup/validate', headers=headers, json=data)
    try:
        errors = response.json()["errors"]
        if "signup_minireg[email]" in errors and errors["signup_minireg[email]"].startswith("We already know this e-mail address."):
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

def deliveroo(email):

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, application/vnd.api+json',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Roo-Client': 'orderweb-client',
        'X-Roo-Country': 'fr',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://deliveroo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"email_address":"tazeest@gmail.com"}'

    response = requests.post('https://consumer-ow-api.deliveroo.com/orderapp/v1/check-email', headers=headers, data=data)
    if response.status_code==200:
        data=response.json()
        if data["registered"]==True:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
def dominosfr(email):
    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://commande.dominos.fr/eStore/fr/Signup',
    }

    s.get("https://commande.dominos.fr/eStore/fr/Signup",headers=headers)
    headers['X-Requested-With'] = 'XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = requests.get('https://commande.dominos.fr/eStore/fr/Signup/IsEmailAvailable', headers=headers, params=params)
    if response.status_code==200:
        if response.text=="false":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
def cracked_to(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://cracked.to/member.php',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://cracked.to',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r=s.get("https://cracked.to/member.php",headers=headers)
    if "Your request was blocked" in r.text or r.status_code!=200:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'


    params = (
        ('action', 'email_availability'),
    )

    data = {
      'email': email,
      'my_post_key':r.text.split('var my_post_key = "')[1].split('"')[0]
    }

    response = s.post('https://cracked.to/xmlhttp.php', headers=headers, params=params, data=data)
    if "Your request was blocked" not in response.text and response.status_code==200:
        if "email address that is already in use by another member." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
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


def imgur(email):
    s=requests.session()

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://imgur.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }


    r=requests.get("https://imgur.com/register?redirect=%2Fuser",headers=headers)


    headers["X-Requested-With"]="XMLHttpRequest"

    data = {
      'email': email
    }

    response = s.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)
    if response.status_code==200:
        if response.json()["data"]["available"]==True:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})




def raidforums(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://raidforums.com/member.php',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://raidforums.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r=s.get("https://raidforums.com/member.php",headers=headers)
    if "Your request was blocked" in r.text or r.status_code!=200:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'


    params = (
        ('action', 'email_availability'),
    )

    data = {
      'email': email,
      'my_post_key':r.text.split('var my_post_key = "')[1].split('"')[0]
    }

    response = s.post('https://raidforums.com/xmlhttp.php', headers=headers, params=params, data=data)
    if "Your request was blocked" not in response.text and response.status_code==200:
        if "email address that is already in use by another member." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def quizlet(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
    }

    response = requests.get("https://quizlet.com/webapi/3.3/validate-email", headers=headers, params={'email': email})

    try:
        existingAccount = response.json()["responses"][0]["data"]["validateEmail"]["existingAccount"]
        return({"rateLimit": False, "exists": existingAccount != None, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def gravatar(email):
    hashed_name =  hashlib.md5(email.encode()).hexdigest()
    r =  requests.get(f'https://gravatar.com/{hashed_name}.json')
    if r.status_code != 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        try:
            data = r.json()
            name = data['entry'][0]['name'].get('formatted')
            others = {
                'FullName': name,
            }

            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": others})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def main():
    print('Github : https://github.com/megadose/holehe')
    start_time = time.time()
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    parser.add_argument(
        "-e",
        "--email",
        help="Email of the target",
        required=True)
    args = parser.parse_args()

    def websiteName(WebsiteFunction, Websitename, email):
        return({Websitename: WebsiteFunction(email)})

    websites = [
        sevencups,
        aboutme,
        adobe,
        amazon,
        anydo,
        atlassian,
        bitmoji,
        blablacar,
        blip,
        buymeacoffe,
        codecademy,
        codepen,
        coroflot,
        cracked_to,
        deliveroo,
        demonforums,
        discord,
        dominosfr,
        ebay,
        ello,
        envato,
        eventbrite,
        evernote,
        facebook,
        firefox,
        freelancer,
        github,
        google,
        gravatar,
        instagram,
        imgur,
        issuu,
        lastfm,
        lastpass,
        live,
        mail_ru,
        myspace,
        nike,
        odnoklassniki,
        office365,
        pinterest,
        plurk,
        pornhub,
        quizlet,
        raidforums,
        rambler,
        redtube,
        samsung,
        snapchat,
        spotify,
        strava,
        taringa,
        teamtreehouse,
        tumblr,
        twitter,
        venmo,
        voxmedia,
        vrbo,
        wordpress,
        xing,
        yahoo]

    que = queue.Queue()
    infos = {}
    threads_list = []

    for website in websites:
        t = Thread(
            target=lambda q, arg1: q.put(
                websiteName(
                    website, website.__name__, args.email)), args=(
                que, website))
        t.start()
        threads_list.append(t)

    for t in tqdm(threads_list):
        t.join()

    while not que.empty():
        result = que.get()
        key, value = next(iter(result.items()))
        infos[key] = value

    description = colored("Email used",
                          "green") + "," + colored(" Email not used",
                                                   "magenta") + "," + colored(" Rate limit",
                                                                              "red")
    print("\033[H\033[J")
    print("*" * 25)
    print(args.email)
    print("*" * 25)
    for i in sorted(infos):
        key, value = i, infos[i]
        i = value
        if i["rateLimit"] == True:
            websiteprint = colored(key, "red")
        elif i["exists"] == False:
            websiteprint = colored(key, "magenta")
        else:
            toprint = ""
            if i["emailrecovery"] is not None:
                toprint += " " + i["emailrecovery"]
            if i["phoneNumber"] is not None:
                toprint += " / " + i["phoneNumber"]
            if i["others"] is not None:
                toprint += " / FullName " + i["others"]["FullName"]

            websiteprint = colored(str(key) + toprint, "green")
        print(websiteprint)

    print("\n" + description)
    print(str(len(websites)) + " websites checked in " +
          str(round(time.time() - start_time, 2)) + " seconds")
