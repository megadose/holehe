# Holehe
<a href="https://www.buymeacoffee.com/megadose" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
# Educational purposes only

### If you have any suggestions, please do not hesitate to contact us.

holehe allows you to check if the mail is used on different sites like twitter, instagram and will retrieve information on sites with the forgotten password function.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Project example : [Holehe Maltego](https://github.com/megadose/holehe-maltego)

### Demo

![](https://github.com/megadose/gif-demo/raw/master/holehe-demo.gif)

## 💡 Prerequisite

   [Python 2/3](https://www.python.org/downloads/release/python-370/)

## 🛠️ Installation

### With PyPI

```pip3 install holehe```

### With Github

```bash
git clone https://github.com/megadose/holehe.git
cd holehe/
python3 setup.py install
```

## 📚 Example

```bash
holehe -e test@gmail.com
```

## 📈 Usage

```python
from holehe import *
print(adobe("test@gmail.com"))
print(lastpass("test@gmail.com"))
```

## Modules :
|  Module     |    Website     |      Method       | Frequent rate limit |
| :-------:   | :-----------:  | :---------------: | :-----------------: |
|  sevencups  |   7cups.com    |     register      |          ✔          |
|  aboutme    |   about.me     |     register      |          ✘          |
|   adobe     |   adobe.com    | password recovery |          ✘          |
|  amazon     |  amazon.com    |       login       |          ✘          |
|  bitmoji    |  bitmoji.com   |       login       |          ✘          |
| blablacar   | blablacar.com  |     register      |          ✔          |
|    blip     |     blip.fm    |     register      |          ✔          |
|buymeacoffee |buymeacoffee.com|     register      |          ✔          |
| codecademy  | codecademy.com |     register      |          ✔          |
|  codepen    |   codepen.io   |     register      |          ✘          |
|copaindavant |linternaute.com | password recovery |          ✘          |
|  coroflot   |  coroflot.com  |     register      |          ✘          |
|  discord    |  discord.com   |     register      |          ✘          |
|   ebay      |   ebay.com     |       login       |          ✔          |
|   ello      |    ello.co     |     register      |          ✘          |
|  envato     |   envato.com   |     register      |          ✘          |
| eventbrite  | eventbrite.com |       login       |          ✘          |
| evernote    | evernote.com   |       login       |          ✘          |
| facebook    | facebook.com   | password recovery |          ✘          |
|  firefox    |  firefox.com   |     register      |          ✘          |
|freelancer   | freelancer.com |     register      |          ✘          |
|  github     |  github.com    |     register      |          ✘          |
| google      |   google.com   |     register      |          ✘          |
| instagram   | instagram.com  |     register      |          ✔          |
|  issuu      |   issuu.com    |     register      |          ✘          |
|  laposte    |    laposte.fr  | password recovery |          ✘          |
|  lastfm     |    last.fm     |     register      |          ✘          |
| lastpass    | lastpass.com   |     register      |          ✘          |
|   live      |   live.com     | password recovery |          ✘          |
|   mail.ru   |    mail.ru     | password recovery |          ✘          |
|   nike      |     nike.com   |     register      |          ✘          |
|odnoklassniki|    ok.ru       | password recovery |          ✘          |
| office365   | office365.com  |       other       |          ✘          |
| pinterest   | pinterest.com  |     register      |          ✘          |
|   plurk     |    plurk.com   |     register      |          ✘          |
|  pornhub    |   pornhub.com  |     register      |          ✘          |
|  quizlet    |   quizlet.com  |     register      |          ✘          |
|  rambler    |   rambler.ru   |     register      |          ✘          |
|   redtube   |   redtube.com  |     register      |          ✘          |
|  samsung    |  samsung.com   |     register      |          ✘          |
|  snapchat   |  snapchat.com  |       login       |          ✘          |
|   spotify   |  spotify.com   |     register      |          ✔          |
|  taringa    |  taringa.net   |     register      |          ✔          |
|teamtreehouse|teamtreehouse.com|     register     |          ✘          |
|  tumblr     |  tumblr.com    |     register      |          ✘          |
|  twitter    |  twitter.com   |     register      |          ✘          |
|   venmo     |   venmo.com    |    register       |          ✔          |
|  voxmedia   | voxmedia.com   |     register      |          ✘          |
|   vrbo      |   vrbo.com     |     register      |          ✘          |
| wordpress   | wordpress.com  |       login       |          ✘          |
|   xing      |   xing.com     |     register      |          ✘          |
|   yahoo     |   yahoo.com    |       login       |          ✔          |

### Rate limit, just change your IP

## The output of the modules

The result of the modules is in this form : `` {"rateLimit":False,"exists":True,"emailrecovery":ex****e@gmail.com,"phoneNumber":'0************78","others":None}``

- rateLitmit : is to find out if you've been rate-limited
- exists : know an account is associated with the mail
- emailrecovery : it's a partial mail that can potentially be extracted from the mail entered on the module.
- phoneNumber : it's a partial phone number that can potentially be extracted from the mail entered on the module.
- others : is used for all information other for the moment it is only useful for facebook ``{"FullName":full_name,"profilePicture":profile_picture}`` FullName has a lot of false positives, and profilePicture is the url of the profile picture associated with the account.

## Thank you to :

- [ navlys ](https://twitter.com/navlys_/)
- [Chris](https://twitter.com/chris_kirsch)
- [socialscan](https://pypi.org/project/socialscan/)
- [UhOh365](https://github.com/Raikia/UhOh365)

## 📝 License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
