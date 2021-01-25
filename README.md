# Holehe Educational purposes only
![PyPI](https://img.shields.io/pypi/v/holehe) ![PyPI - Week](https://img.shields.io/pypi/dw/holehe) ![PyPI - Downloads](https://static.pepy.tech/badge/holehe) ![PyPI - License](https://img.shields.io/pypi/l/holehe)
#### For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ
### Holehe [does not alert the target email](https://github.com/megadose/holehe/issues/12)
holehe allows you to check if the mail is used on different sites like twitter, instagram and will retrieve information on sites with the forgotten password function.

![](https://files.catbox.moe/5we2ya.png)

![](https://github.com/megadose/gif-demo/raw/master/holehe-demo.gif)
## Project example : [Holehe Maltego](https://github.com/megadose/holehe-maltego)
## 💡 Prerequisite

   [Python 3](https://www.python.org/downloads/release/python-370/)

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
holehe test@gmail.com
```


### Rate limit, just change your IP

## 📈 Example of use

```python
import trio
import httpx

from holehe.modules.shopping.ebay import ebay


async def main():
    email = "test@gmail.com"
    out = []
    client = httpx.AsyncClient()

    await ebay(email, client, out)

    print(out)
    await client.aclose()

trio.run(main)
```


## The output of the modules

The result of the modules is in this form : `` {name:"example","rateLimit":False,"exists":True,"emailrecovery":ex****e@gmail.com,"phoneNumber":'0************78","others":None}``

- rateLitmit : is to find out if you've been rate-limited
- exists : know an account is associated with the mail
- emailrecovery : it's a partial mail that can potentially be extracted from the mail entered on the module.
- phoneNumber : it's a partial phone number that can potentially be extracted from the mail entered on the module.
- others : is used for all information other

## Thank you to :

- [navlys](https://twitter.com/navlys_/)
- [Chris](https://twitter.com/chris_kirsch)
- [socialscan](https://pypi.org/project/socialscan/)
- [UhOh365](https://github.com/Raikia/UhOh365)
- [soxoj](https://github.com/soxoj)
- [mxrch](https://github.com/mxrch)

## 📝 License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)

## Modules :
| name                | domain                                 | method            | frequent_rate_limit |
| ------------------- | -------------------------------------- | ----------------- | ------------------- |
| aboutme             | about.me                               | register          | ✘               |
| adobe               | adobe.com                              | password recovery | ✘               |
| amazon              | amazon.com                             | login             | ✘               |
| anydo               | any.do                                 | login             | ✔               |
| archive             | archive.org                            | register          | ✘               |
| armurerieauxerre    | armurerie-auxerre.com                  | register          | ✘               |
| atlassian           | atlassian.com                          | register          | ✘               |
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
| google              | google.com                             | register          | ✘               |
| gravatar            | gravatar.com                           | other             | ✘               |
| imgur               | imgur.com                              | register          | ✔               |
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
| odampublishing      | forum.odampublishing.com               | register          | ✘               |
| odnoklassniki       | ok.ru                                  | password recovery | ✘               |
| office365           | office365.com                          | other             | ✘               |
| onlinesequencer     | onlinesequencer.net                    | register          | ✘               |
| parler              | parler.com                             | login             | ✘               |
| patreon             | patreon.com                            | login             | ✔               |
| pinterest           | pinterest.com                          | register          | ✘               |
| plurk               | plurk.com                              | register          | ✘               |
| pornhub             | pornhub.com                            | register          | ✘               |
| protonmail          | protonmail.ch                          | other             | ✘               |
| quora               | quora.com                              | register          | ✘               |
| raidforums          | raidforums.com                         | register          | ✔               |
| rambler             | rambler.ru                             | register          | ✘               |
| redtube             | redtube.com                            | register          | ✘               |
| replit              | repl.it                                | register          | ✔               |
| rocketreach         | rocketreach.co                         | register          | ✘               |
| samsung             | samsung.com                            | register          | ✘               |
| seoclerks           | seoclerks.com                          | register          | ✘               |
| sevencups           | 7cups.com                              | register          | ✔               |
| smule               | smule.com                              | register          | ✔               |
| snapchat            | snapchat.com                           | login             | ✘               |
| sporcle             | sporcle.com                            | register          | ✘               |
| spotify             | spotify.com                            | register          | ✔               |
| strava              | strava.com                             | register          | ✘               |
| taringa             | taringa.net                            | register          | ✔               |
| teamtreehouse       | teamtreehouse.com                      | register          | ✘               |
| tellonym            | tellonym.me                            | register          | ✘               |
| thecardboard        | thecardboard.org                       | register          | ✘               |
| therianguide        | forums.therian-guide.com               | register          | ✘               |
| thevapingforum      | thevapingforum.com                     | register          | ✘               |
| treasureclassifieds | forum.treasureclassifieds.com          | register          | ✘               |
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
| xvideos             | xvideos.com                            | register          | ✘               |
| yahoo               | yahoo.com                              | login             | ✔               |
