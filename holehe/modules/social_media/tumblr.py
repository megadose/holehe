from holehe.core import *
from holehe.localuseragent import *


async def tumblr(email, client, out):
    name = "tumblr"
    domain = "tumblr.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    firstreq = await client.get("https://www.tumblr.com/login", headers=headers)
    data = {
        'determine_email': email, 'user[email]': '', 'user[password]': '',
        'tumblelog[name]': '', 'user[age]': '', 'context': 'no_referer',
        'version': 'STANDARD', 'follow': '',
        'form_key': firstreq.text.split(
            '<meta name="tumblr-form-key" id="tumblr_form_key" content="')
        [1].split('"')[0],
        'seen_suggestion': '0', 'used_suggestion': '0',
        'used_auto_suggestion': '0', 'about_tumblr_slide': '',
        'random_username_suggestions': firstreq.text.split(
            'id="random_username_suggestions" name="random_username_suggestions" value="')
        [1].split('"')[0],
        'action': 'signup_determine', 'action': 'signup_determine',
        'tracking_url': '/login', 'tracking_version': 'modal', }
    response = await client.post('https://www.tumblr.com/svc/account/register', data=data, headers=headers)
    if response.text == '{"redirect":false,"redirect_method":"GET","errors":[],"signup_success":false,"next_view":"signup_magiclink"}':
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
