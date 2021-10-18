from holehe.core import *
from holehe.localuseragent import *

async def xnxx(email, client, out):
    name = "xnxx"
    domain = "xnxx.com"
    method= "register"
    frequent_rate_limit=True

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-fr',
        'Host': 'www.xnxx.com',
        'User-Agent': random.choice(ua["browsers"]["safari"]),
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'}

    XNXX = await client.get('https://www.xnxx.com', headers=headers)
    if XNXX.status_code == 200:
        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        
        email = email.replace('@', '%40')
        APIRQST = await client.get(f'https://www.xnxx.com/account/checkemail?email={email}', headers=headers, cookies=XNXX.cookies)
        if APIRQST.status_code == 200:
            API = json.loads(APIRQST.text)

            if API['result'] == False and API['code'] == 1 and API['message'] == 'Cet email est d&eacute;j&agrave; utilis&eacute; ou son propri&eacute;taire l&#039;a exclu de notre site.':
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

            elif API['result'] == False and API['code'] == 1 and API['message'] == 'Adresse email invalide.':
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

            elif API['result'] == True and API['code'] == 0:
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

            elif API['result'] == False and API['code'] == 2 and API['message'] == 'Trop rapide. Merci de r&eacute;essayer dans quelques secondes.':
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
