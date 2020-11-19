from holehe.core import *
from holehe.localuseragent import *


def amazon(email):
    brows = Browser()
    brows.set_handle_robots(False)
    brows._factory.is_html = True
    brows.set_cookiejar(cookielib.LWPCookieJar())
    brows.addheaders = [
        ('User-agent',
         random.choice(
             ua["browsers"]["chrome"]))]
    brows.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(),
        max_time=1)
    url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    brows.open(url, timeout=10)
    brows.select_form(nr=0)
    brows.form['email'] = email

    brows.method = "POST"
    submit = brows.submit()
    soup = BeautifulSoup(submit.read().decode("utf-8"), "lxml")
    if soup.find("div", {"id": "auth-password-missing-alert"}):
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
