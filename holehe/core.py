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
import importlib
import pkgutil

from tqdm import tqdm
from termcolor import colored
from threading import Thread
from bs4 import BeautifulSoup
from mechanize import Browser

"""
from modules.programing.codeacademy import *
from modules.commerce import *
from modules.porn import *
from modules.cms import *
from modules.development import *
"""

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib

from holehe.localuseragent import *
from modules import *

def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages
    :param recursive: bool
    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    print(results)
    return results

modules = import_submodules("modules")

websites = list()

for module in modules:
    if len(module.split(".")) > 2:
        modu = modules[module]
        site = module.split(".")[-1]
        websites.append(modu.__dict__[site])


#from modules.medical.sevencups import sevencups

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
    'Google-Accounts-XSRF': '1',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    'Origin': 'https://accounts.google.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2F&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp',
    'TE': 'Trailers',
    }

    s=requests.session()
    req = s.get(
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
    'continue': 'https://accounts.google.com/',
    'dsh': '',
    'hl': 'fr',
    'f.req': '["' + freq + '","","","' + email + '",false]',
    'azt': '',
    'cookiesDisabled': 'false',
    'deviceinfo': '[null,null,null,[],null,"FR",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,null,0,null,false]',
    'gmscoreversion': 'undefined',
    '': ''

    }
    response = s.post('https://accounts.google.com/_/signup/webusernameavailability', headers=headers, params=params, data=data)
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
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
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

def laposte(email):
    headers = {
        'Origin': 'https://www.laposte.fr',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.laposte.fr/authentification',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'email': email,
        'customerId': '',
        'tunnelSteps': ''
        }

    response = requests.post('https://www.laposte.fr/authentification', headers=headers, data=data)
    post_soup = BeautifulSoup(response.content , 'lxml')
    l = post_soup.find_all('span', id="wrongEmail")
    return({"rateLimit": False, "exists": l != [], "emailrecovery": None, "phoneNumber": None, "others": None})

def crevado(email):
    s=requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://crevado.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    req=s.get("https://crevado.com")
    token=req.text.split('<meta name="csrf-token" content="')[1].split('"')[0]

    data = [
      ('utf8', '\u2713'),
      ('authenticity_token', token),
      ('plan', 'basic'),
      ('account[full_name]', ''),
      ('account[email]', email),
      ('account[password]', ''),
      ('account[domain]', ''),
      ('account[confirm_madness]', ''),
      ('account[terms_accepted]', '0'),
      ('account[terms_accepted]', '1'),
    ]

    response = s.post('https://crevado.com/', headers=headers, data=data)
    try:
        msg_error=response.text.split('showFormErrors({"')[1].split('"')[0]
        if msg_error=="account_email":
            errorEMail=response.text.split('showFormErrors({"account_email":{"error_message":"')[1].split('"')[0]
            if errorEMail=="has already been taken":
                return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except :
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


def gravatar(email):
    hashed_name =  hashlib.md5(email.encode()).hexdigest()
    r =  requests.get('https://gravatar.com/{hashed_name}.json')
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


print("coucou")


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

main()
