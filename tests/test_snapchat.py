import asyncio
import unittest

import httpx

from holehe.modules.social_media.snapchat import snapchat


class MissingTokenClient:
    async def get(self, _url):
        return httpx.Response(200, text="<html>No login markers.</html>")


class SnapchatTests(unittest.TestCase):
    def test_reports_rate_limit_when_login_tokens_are_missing(self):
        out = []

        asyncio.run(snapchat("user@example.com", MissingTokenClient(), out))

        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "snapchat")
        self.assertTrue(out[0]["rateLimit"])
        self.assertFalse(out[0]["exists"])
