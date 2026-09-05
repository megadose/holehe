# **MailScope OSINT - Email to Registered Accounts**

MailScope checks if an email is attached to an account across more than 120 websites (Twitter, Instagram, Imgur, and more) with intelligent rate-limit mitigation and proxy rotation.

+ Retrieves information using the forgotten password function.
+ **Does not alert the target email.**
+ **Aggressive HTTP 429 Mitigation**: Low-concurrency worker ceiling (default 2 workers, `--sequential`), randomized human-like jitter pacing (0.5s–1.8s), and automatic exponential backoff retry.
+ **Proxy & IP Rotation**: Route requests through `--proxy` (HTTP/SOCKS5) or `--proxy-file` with round-robin distribution and instant rotation on connection block/429.
+ **Module Filtering & Inspection**: Filter via `--only`, `--exclude`, and list all modules via `--list-sites`.

## 🛠️ Installation

```bash
git clone https://github.com/megadose/holehe.git
cd holehe/
pip install -e .
```

## Quick Start

### 📚 CLI Examples

```bash
# Basic run
mailscope target@example.com

# Sequential execution with strict rate limit defense
mailscope target@example.com --sequential

# Single HTTP or SOCKS5 proxy
mailscope target@example.com --proxy socks5://127.0.0.1:1080

# Proxy rotation pool (rotates round-robin and on HTTP 429 / connection block)
mailscope target@example.com --proxy-file proxies.txt

# Run checks only on specific sites
mailscope target@example.com --only twitter instagram spotify

# Exclude specific sites
mailscope target@example.com --exclude adobe samsung

# List all available modules
mailscope --list-sites
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
