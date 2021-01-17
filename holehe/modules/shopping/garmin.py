from holehe.core import *
from holehe.localuseragent import *


async def garmin(email, client, out):
    name = "garmin"
    domain = "garmin.com"
    method = "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    params = (
        ('service', 'https://www.garmin.com/fr-FR/account/profile/'),
        ('webhost', 'https://www.garmin.com/fr-FR/account/create/'),
        ('source', 'https://www.garmin.com/fr-FR/account/create/'),
        ('redirectAfterAccountLoginUrl', 'https://www.garmin.com/fr-FR/account/profile/'),
        ('redirectAfterAccountCreationUrl', 'https://www.garmin.com/fr-FR/account/profile/'),
        ('gauthHost', 'https://sso.garmin.com/sso'),
        ('id', 'js__app__create__gauth-widget'),
        ('cssUrl', 'https://www.garmin.com/account/ui/css/create-account-v1.12.3-min.css'),
        ('clientId', 'ACCOUNT_MANAGEMENT_CENTER'),
        ('rememberMeShown', 'true'),
        ('rememberMeChecked', 'undefined'),
        ('createAccountShown', 'true'),
        ('openCreateAccount', 'true'),
        ('displayNameShown', 'false'),
        ('consumeServiceTicket', 'true'),
        ('initialFocus', 'true'),
        ('embedWidget', 'false'),
        ('generateExtraServiceTicket', 'true'),
        ('generateTwoExtraServiceTickets', 'false'),
        ('generateNoServiceTicket', 'false'),
        ('globalOptInShown', 'true'),
        ('globalOptInChecked', 'false'),
        ('mobile', 'false'),
        ('connectLegalTerms', 'false'),
        ('showTermsOfUse', 'false'),
        ('showPrivacyPolicy', 'false'),
        ('showConnectLegalAge', 'false'),
        ('locationPromptShown', 'false'),
        ('showPassword', 'true'),
        ('useCustomHeader', 'false'),
        ('mfaRequired', 'false'),
        ('rememberMyDeviceShown', 'false'),
        ('rememberMyDeviceChecked', 'false'),
    )

    params = dict(params)

    try:
        req = await client.get('https://sso.garmin.com/sso/createNewAccount', headers=headers, params=params)
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    try:
        token = req.text.split('"token": "')[1].split('"')[0]
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    headers["Origin"] = "https://sso.garmin.com"
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    params = {
        'clientId': '',
        'locale': '',
    }
    data = {
        'email': email,
        'token': token
    }
    req = await client.post('https://sso.garmin.com/sso/validateNewAccount', headers=headers, params=params, data=data)
    if req.text == "false":
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif req.text == "true":
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
