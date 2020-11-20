from holehe.core import *
from holehe.localuseragent import *
def garmin(email):
    s=requests.session()

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

    response = s.get('https://sso.garmin.com/sso/createNewAccount', headers=headers, params=params)
    try:
        token=response.text.split('"token": "')[1].split('"')[0]
    except:
        return({"rateLimit": True,"exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers["X-Requested-With"]= 'XMLHttpRequest'

    params = (
        ('clientId', 'ACCOUNT_MANAGEMENT_CENTER'),
    )

    data = {
      'email': email,
      'token': token
    }

    response = s.post('https://sso.garmin.com/sso/validateNewAccount', headers=headers, params=params, data=data)
    if response.text=="false":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text=="true":
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True,"exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
