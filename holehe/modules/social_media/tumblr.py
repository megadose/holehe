from holehe.core import *
from holehe.localuseragent import *
from string import ascii_lowercase, printable

async def tumblr(email, client, out):
    name = "tumblr"
    domain = "tumblr.com"
    method = "register"
    frequent_rate_limit=False

    usrag = random.choice(ua["browsers"]["iOS"])

    try:
        getBearer = await client.get("https://www.tumblr.com/", headers={
            "Host": "www.tumblr.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": usrag
        })
        if getBearer.status_code != 200:
            raise Exception("xc")
        
        p = BeautifulSoup(getBearer.text,"html.parser").find_all("script")
        bearer = [";".join(elem.text.split("window['___INITIAL_STATE___'] = ")[-1].split(";")[:-1]).split('{"API_TOKEN":"')[-1].split('","extraHeaders":"{}"}')[0] for elem in p if "window['___INITIAL_STATE___']" in elem.text][0]
        bearer = f"Bearer {bearer}"

        getCsrf = await client.get("https://www.tumblr.com/api/v2/radar?fields%5Bblogs%5D=name%2Cavatar%2Cdescription%2Ctheme%2Ctitle%2Curl%2Cuuid%2Ccan_message%2Ccan_be_followed%2Cis_adult&limit=15", headers={
            "Host": "www.tumblr.com",
            "X-Ad-Blocker-Enabled": "0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "X-Version": "redpop/3/0//redpop/",
            "Accept": "application/json;format=camelcase",
            "User-Agent": usrag,
            "Accept-Language": "fr-fr",
            "Authorization": bearer,
            "Referer": "https://www.tumblr.com/"
        })
        if getCsrf.status_code != 200:
            raise Exception("xc")
        csrf = getCsrf.headers["X-Csrf"]

        data = json.dumps({
            "password": "".join([random.choice(ascii_lowercase) for _ in range(random.randint(2,5))]),
            "email": email,
            "tumblelog": "".join([random.choice(printable) for _ in range(random.randint(6,12))])
            }, indent=2)
        post = await client.post("https://www.tumblr.com/api/v2/register/account/validate", headers={
            "Host": "www.tumblr.com",
            "Accept": "application/json;format=camelcase",
            "Authorization": bearer,
            "X-CSRF": csrf,
            "X-Version": "redpop/3/0//redpop/",
            "Content-Type": "application/json; charset=utf8",
            "Accept-Language": "fr-fr",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://www.tumblr.com",
            "User-Agent": usrag,
            "Content-Length": f"{len(data)}",
            "Referer": "https://www.tumblr.com/register?source=login_register_center",
            "X-Ad-Blocker-Enabled": "0",
            "Connection": "close",
            "Cookie": "palette=trueBlue; tz=Europe%2FParis"
        }, cookies={
            "palette":"trueBlue",
            "tz":"Europe%2FParis"},
        data=data
        )

        if post.status_code != 400:
            raise Exception("xc")
        error = post.json()["response"]["code"]
        if error == 2: # L'erreur 2 "User already exists" apparait en priorité sur l'erreur 1030 "Password must be at least 8 characters long"
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

        elif error == 1030:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

        else: #429 {"meta":{"status":429,"msg":"Limit Exceeded"},"response":[]}
            raise Exception("xc")

    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
