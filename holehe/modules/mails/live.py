from holehe.core import *
from holehe.localuseragent import *


def live(email):
    brows = Browser()
    brows.set_handle_robots(False)
    brows._factory.is_html = True
    brows.set_cookiejar(cookielib.LWPCookieJar())
    brows.addheaders = [
        ('User-agent',
         random.choice(
             ua["browsers"]["firefox"]))]
    brows.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(), max_time=1)
    url = "https://account.live.com/password/reset"
    brows.open(url, timeout=10)
    brows.select_form(nr=0)
    brows.form['iSigninName'] = email
    brows.method = "POST"
    submit = brows.submit()
    try:
        datatext=str('{"name":"' + str(submit.read().decode("utf-8")).split('"},{"name":"')[1].split('],"showExpirationCheckbox')[0])
    except IndexError:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    if "},{" in datatext:
        data1=json.loads(datatext.split("},{")[0]+"}")
        data2=json.loads("{"+datatext.split("},{")[1])
        if "@" in data1["name"]:
            return({"rateLimit": False, "exists": True, "emailrecovery": data1["name"], "phoneNumber": data2["name"], "others": None})
        elif "@" in data2["name"]:
            return({"rateLimit": False, "exists": True, "emailrecovery": data2["name"], "phoneNumber": data1["name"], "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data1["name"], "others": None})
    data = json.loads(datatext)
    if data["type"] == "Email":
        return({"rateLimit": False, "exists": True, "emailrecovery": data["name"], "phoneNumber": None, "others": None})
    elif data["type"] == "Sms":
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data["name"], "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": data2["name"], "others": None})
