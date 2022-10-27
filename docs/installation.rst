Installation
=============



==========   ======================================
Platform     Command
==========   ======================================
PyPi          ``pip3 install holehe``
Github           ``git clone https://github.com/megadose/holehe.git``
==========   ======================================

Quick Start
============

Holehe can be run from the CLI and rapidly embedded within existing python applications.

Cli Example
^^^^^^^^^^^
::

    holehe test@gmail.com

Python Example
^^^^^^^^^^^^^^^
::

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

.. image:: https://github.com/megadose/gif-demo/raw/master/holehe-demo.gif

Module Output
^^^^^^^^^^^^^^^

For each module, data is returned in a standard dictionary with the following json-equivalent format :

::

    {
      "name": "example",
      "rateLimit": false,
      "exists": true,
      "emailrecovery": "ex****e@gmail.com",
      "phoneNumber": "0*******78",
      "others": null
    }


* rateLitmit : Lets you know if you've been rate-limited.
* exists : If an account exists for the email on that service.
* emailrecovery : Sometimes partially obfuscated recovery emails are returned.
* phoneNumber : Sometimes partially obfuscated recovery phone numbers are returned.
* others : Any extra info.

* Rate limit? Change your IP.



