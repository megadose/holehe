<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random

from holehe import *
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

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
