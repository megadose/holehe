import requests
import random
import json

from bs4 import BeautifulSoup
from holehe.localuseragent import ua

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
