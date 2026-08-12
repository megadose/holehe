# **Holehe OSINT - Sddhrthgrv@gmail.com**
👋 Hi there! For any professional inquiries or collaborations, please reach out to me at:
megadose@protonmail.com

📧 Preferably, use your professional email for correspondence. Let's keep it short and sweet, and all in English!

![](https://files.catbox.moe/5we2ya.png)
![PyPI](https://img.shields.io/pypi/v/holehe) ![PyPI - Week](https://img.shields.io/pypi/dw/holehe) ![PyPI - Downloads](https://static.pepy.tech/badge/holehe) ![PyPI - License](https://img.shields.io/pypi/l/holehe)

# [Holehe Online Version](https://osint.industries/)

## **Summary**

*Efficiently finding registered accounts from emails.*

Holehe checks if an email is attached to an account on sites like twitter, instagram, imgur and more than 120 others.

+ Retrieves information using the forgotten password function.
+ **[Does not alert the target email.](https://github.com/megadose/holehe/issues/12)**
+ Runs on [Python 3](https://www.python.org/downloads/release/python-370/).
## 🛠️ Installation

### With PyPI

```pip3 install holehe```

### With Github

```bash
git clone https://github.com/megadose/holehe.git
cd holehe/
python3 setup.py install
```

### With Docker

```bash
docker build . -t my-holehe-image
docker run my-holehe-image holehe test@gmail.com
```

## Quick Start

Holehe can be run from the CLI and rapidly embedded within existing python applications.
### 📚 CLI Example

```bash
holehe test@gmail.com
```
### 📈 Python Example

```python
import trio
import httpx

from holehe.modules.social_media.snapchat import snapchat


async def main():
    email = "test@gmail.com"
    out = []
    client = httpx.AsyncClient()

    await snapchat(email, client, out)

    print(out)
    await client.aclose()

trio.run(main)
```
![](https://github.com/megadose/gif-demo/raw/master/holehe-demo.gif)
## Module Output

For each module, data is returned in a standard dictionary with the following json-equivalent format :
```json
{
  "name": "example",
  "rateLimit": false,
  "exists": true,
  "emailrecovery": "ex****e@gmail.com",
  "phoneNumber": "0*******78",
  "others": null
}
```

- rateLitmit : Lets you know if you've been rate-limited.
- exists : If an account exists for the email on that service.
- emailrecovery : Sometimes partially obfuscated recovery emails are returned.
- phoneNumber : Sometimes partially obfuscated recovery phone numbers are returned.
- others : Any extra info.


Rate limit? Change your IP.


## Maltego Transform : [Holehe Maltego](https://github.com/megadose/holehe-maltego)

## Thank you to :

- [navlys](https://twitter.com/navlys_/)
- [Chris](https://twitter.com/chris_kirsch)
- [socialscan](https://pypi.org/project/socialscan/)
- [UhOh365](https://github.com/Raikia/UhOh365)
- [soxoj](https://github.com/soxoj)
- [mxrch](https://github.com/mxrch) (and for the logo)
- [novitae](https://github.com/novitae)

## Donations

For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ

## 📝 License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)

Built for educational purposes only.

## Modules
| Name                | Domain                                 | Method            | Frequent Rate Limit |
| ------------------- | -------------------------------------- | ----------------- | ------------------- |
| aboutme             | about.me                               | register          | ✘               |
| adobe               | adobe.com                              | password recovery | ✘               |
| amazon              | amazon.com                             | login             | ✘               |
| amocrm              | amocrm.com                             | register          | ✘               |
| anydo               | any.do                                 | login             | ✔               |
| archive             | archive.org                            | register          | ✘               |
| armurerieauxerre    | armurerie-auxerre.com                  | register          | ✘               |
| atlassian           | atlassian.com                          | register          | ✘               |
| axonaut             | axonaut.com                            | register          | ✘               |
| babeshows           | babeshows.co.uk                        | register          | ✘               |
| badeggsonline       | badeggsonline.com                      | register          | ✘               |
| biosmods            | bios-mods.com                          | register          | ✘               |
| biotechnologyforums | biotechnologyforums.com                | register          | ✘               |
| bitmoji             | bitmoji.com                            | login             | ✘               |
| blablacar           | blablacar.com                          | register          | ✔               |
| blackworldforum     | blackworldforum.com                    | register          | ✔               |
| blip                | blip.fm                                | register          | ✔               |
| blitzortung         | forum.blitzortung.org                  | register          | ✘               |
| bluegrassrivals     | bluegrassrivals.com                    | register          | ✘               |
| bodybuilding        | bodybuilding.com                       | register          | ✘               |
| buymeacoffee        | buymeacoffee.com                       | register          | ✔               |
| cambridgemt         | discussion.cambridge-mt.com            | register          | ✘               |
| caringbridge        | caringbridge.org                       | register          | ✘               |
| chinaphonearena     | chinaphonearena.com                    | register          | ✘               |
| clashfarmer         | clashfarmer.com                        | register          | ✔               |
| codecademy          | codecademy.com                         | register          | ✔               |
| codeigniter         | forum.codeigniter.com                  | register          | ✘               |
| codepen             | codepen.io                             | register          | ✘               |
| coroflot            | coroflot.com                           | register          | ✘               |
| cpaelites           | cpaelites.com                          | register          | ✘               |
| cpahero             | cpahero.com                            | register          | ✘               |
| cracked_to          | cracked.to                             | register          | ✔               |
| crevado             | crevado.com                            | register          | ✔               |
| deliveroo           | deliveroo.com                          | register          | ✔               |
| demonforums         | demonforums.net                        | register          | ✔               |
| devrant             | devrant.com                            | register          | ✘               |
| diigo               | diigo.com                              | register          | ✘               |
| discord             | discord.com                            | register          | ✘               |
| docker              | docker.com                             | register          | ✘               |
| dominosfr           | dominos.fr                             | register          | ✔               |
| ebay                | ebay.com                               | login             | ✔               |
| ello                | ello.co                                | register          | ✘               |
| envato              | envato.com                             | register          | ✘               |
| eventbrite          | eventbrite.com                         | login             | ✘               |
| evernote            | evernote.com                           | login             | ✘               |
| fanpop              | fanpop.com                             | register          | ✘               |
| firefox             | firefox.com                            | register          | ✘               |
| flickr              | flickr.com                             | login             | ✘               |
| freelancer          | freelancer.com                         | register          | ✘               |
| freiberg            | drachenhort.user.stunet.tu-freiberg.de | register          | ✘               |
| garmin              | garmin.com                             | register          | ✔               |
| github              | github.com                             | register          | ✘               |
| google              | google.com                             | register          | ✔               |
| gravatar            | gravatar.com                           | other             | ✘               |
| hubspot             | hubspot.com                            | login             | ✘               |
| imgur               | imgur.com                              | register          | ✔               |
| insightly           | insightly.com                          | login             | ✘               |
| instagram           | instagram.com                          | register          | ✔               |
| issuu               | issuu.com                              | register          | ✘               |
| koditv              | forum.kodi.tv                          | register          | ✘               |
| komoot              | komoot.com                             | register          | ✔               |
| laposte             | laposte.fr                             | register          | ✘               |
| lastfm              | last.fm                                | register          | ✘               |
| lastpass            | lastpass.com                           | register          | ✘               |
| mail_ru             | mail.ru                                | password recovery | ✘               |
| mybb                | community.mybb.com                     | register          | ✘               |
| myspace             | myspace.com                            | register          | ✘               |
| nattyornot          | nattyornotforum.nattyornot.com         | register          | ✘               |
| naturabuy           | naturabuy.fr                           | register          | ✘               |
| ndemiccreations     | forum.ndemiccreations.com              | register          | ✘               |
| nextpvr             | forums.nextpvr.com                     | register          | ✘               |
| nike                | nike.com                               | register          | ✘               |
| nimble              | nimble.com                             | register          | ✘               |
| nocrm               | nocrm.io                               | register          | ✘               |
| nutshell            | nutshell.com                           | register          | ✘               |
| odnoklassniki       | ok.ru                                  | password recovery | ✘               |
| office365           | office365.com                          | other             | ✔               |
| onlinesequencer     | onlinesequencer.net                    | register          | ✘               |
| parler              | parler.com                             | login             | ✘               |
| patreon             | patreon.com                            | login             | ✔               |
| pinterest           | pinterest.com                          | register          | ✘               |
| pipedrive           | pipedrive.com                          | register          | ✘               |
| plurk               | plurk.com                              | register          | ✘               |
| pornhub             | pornhub.com                            | register          | ✘               |
| protonmail          | protonmail.ch                          | other             | ✘               |
| quora               | quora.com                              | register          | ✘               |
| rambler             | rambler.ru                             | register          | ✘               |
| redtube             | redtube.com                            | register          | ✘               |
| replit              | replit.com                             | register          | ✔               |
| rocketreach         | rocketreach.co                         | register          | ✘               |
| samsung             | samsung.com                            | register          | ✘               |
| seoclerks           | seoclerks.com                          | register          | ✘               |
| sevencups           | 7cups.com                              | register          | ✔               |
| smule               | smule.com                              | register          | ✔               |
| snapchat            | snapchat.com                           | login             | ✘               |
| soundcloud          | soundcloud.com                         | register          | ✘               |
| sporcle             | sporcle.com                            | register          | ✘               |
| spotify             | spotify.com                            | register          | ✔               |
| strava              | strava.com                             | register          | ✘               |
| taringa             | taringa.net                            | register          | ✔               |
| teamleader          | teamleader.com                         | register          | ✘               |
| teamtreehouse       | teamtreehouse.com                      | register          | ✘               |
| tellonym            | tellonym.me                            | register          | ✘               |
| thecardboard        | thecardboard.org                       | register          | ✘               |
| therianguide        | forums.therian-guide.com               | register          | ✘               |
| thevapingforum      | thevapingforum.com                     | register          | ✘               |
| tumblr              | tumblr.com                             | register          | ✘               |
| tunefind            | tunefind.com                           | register          | ✔               |
| twitter             | twitter.com                            | register          | ✘               |
| venmo               | venmo.com                              | register          | ✔               |
| vivino              | vivino.com                             | register          | ✘               |
| voxmedia            | voxmedia.com                           | register          | ✘               |
| vrbo                | vrbo.com                               | register          | ✘               |
| vsco                | vsco.co                                | register          | ✘               |
| wattpad             | wattpad.com                            | register          | ✔               |
| wordpress           | wordpress                              | login             | ✘               |
| xing                | xing.com                               | register          | ✘               |
| xnxx                | xnxx.com                               | register          | ✔               |
| xvideos             | xvideos.com                            | register          | ✘               |
| yahoo               | yahoo.com                              | login             | ✔               |
| zoho                | zoho.com                               | login             | ✔               |
