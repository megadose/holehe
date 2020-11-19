from holehe.core import *
from holehe.localuseragent import *

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
