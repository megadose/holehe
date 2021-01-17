from holehe.core import *
from holehe.localuseragent import *


async def fetlife(email, client, out):
    name = "fetlife"
    domain = "fetlife.com"
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
    try:
        req = await client.get("https://fetlife.com/signup_step_profile", headers=headers)
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    soup = BeautifulSoup(req.content, features="html.parser")

    inp_method = soup.find(
        "input",
        attrs={
            "type": "hidden",
            "name": "_method"})
    inp_authenticity_token = soup.find(
        "input",
        attrs={"type": "hidden", "name": "authenticity_token"}
    )

    if inp_method is None or inp_authenticity_token is None:
        raise NotImplementedError(
            "Fetlife register page changed, this module need to be updated."
        )

    data = {
        "_method": inp_method.get("value"),
        "authenticity_token": inp_authenticity_token.get("value"),
        "user[nickname]": "",
        "user[email]": email,
        "user[password]": "",
    }

    post = await client.post(
        "https://fetlife.com/signup_step_profile",
        headers=headers,
        data=data
    )
    resp_soup = BeautifulSoup(post.content, features="html.parser")

    EMAIL_MSG_ERROR = (
        "We're having problems processing the above email address. "
        "We recommend you verify the spelling or try a different one."
    )

    email_error_tag = resp_soup.findAll(text=EMAIL_MSG_ERROR)

    email_is_present = len(email_error_tag) > 0

    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                "rateLimit": False,
                "exists": email_is_present,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None})
