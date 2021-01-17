from holehe.core import *
from holehe.localuseragent import *


async def wordpress(email, client, out):
    name = "wordpress"
    domain = "wordpress"
    method= "login"
    frequent_rate_limit=False

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

    params = {
        'http_envelope': '1',
        'locale': 'fr',
    }
    try:
        response = await client.get('https://public-api.wordpress.com/rest/v1.1/users/' + email + '/auth-options', headers=headers, params=params, cookies=cookies)
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    info = response.json()
    if "email_verified" in info["body"].keys():
        if info["body"]["email_verified"]:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    elif "unknown_user" in str(info) or "email_login_not_allowed" in str(info):
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
