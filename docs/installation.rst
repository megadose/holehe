Installation
=========



==========   ======================================
Platform     Command
==========   ======================================
PyPi          ``pip3 install holehe``
Github           ``git clone https://github.com/megadose/holehe.git``
==========   ======================================

Quick Start
=========

Holehe can be run from the CLI and rapidly embedded within existing python applications.

Cli Example
^^^^^^
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
