import asyncio
import unittest

import httpx

from holehe.modules.social_media.imgur import imgur


class ImgurClient:
    def __init__(self, response):
        self.response = response

    async def get(self, _url, **_kwargs):
        return httpx.Response(200, text="<html>registration form</html>")

    async def post(self, _url, **_kwargs):
        return self.response


class ImgurTests(unittest.TestCase):
    def run_imgur(self, response):
        out = []
        asyncio.run(imgur("user@example.com", ImgurClient(response), out))
        return out[0]

    def test_captcha_error_is_rate_limited(self):
        response = httpx.Response(
            200,
            json={
                "data": {"available": False},
                "errors": ["A captcha token is required."],
            },
        )

        result = self.run_imgur(response)

        self.assertTrue(result["rateLimit"])
        self.assertFalse(result["exists"])

    def test_missing_availability_is_rate_limited(self):
        response = httpx.Response(200, json={"data": {"error": "captcha-required"}})

        result = self.run_imgur(response)

        self.assertTrue(result["rateLimit"])
        self.assertFalse(result["exists"])

    def test_api_error_status_is_rate_limited(self):
        response = httpx.Response(
            200,
            json={
                "data": {"available": False},
                "success": False,
                "status": 429,
            },
        )

        result = self.run_imgur(response)

        self.assertTrue(result["rateLimit"])
        self.assertFalse(result["exists"])

    def test_available_email_is_not_reported_as_registered(self):
        response = httpx.Response(200, json={"data": {"available": True}})

        result = self.run_imgur(response)

        self.assertFalse(result["rateLimit"])
        self.assertFalse(result["exists"])

    def test_unavailable_email_is_reported_as_registered(self):
        response = httpx.Response(200, json={"data": {"available": False}})

        result = self.run_imgur(response)

        self.assertFalse(result["rateLimit"])
        self.assertTrue(result["exists"])

    def test_invalid_email_domain_is_not_reported_as_registered(self):
        response = httpx.Response(
            200, text='{"data": {"available": false, "error": "Invalid email domain"}}'
        )

        result = self.run_imgur(response)

        self.assertFalse(result["rateLimit"])
        self.assertFalse(result["exists"])

    def test_captcha_in_email_address_does_not_hide_unavailable_email(self):
        response = httpx.Response(
            200,
            json={"data": {"available": False}, "email": "user@captcha.example"},
        )

        result = self.run_imgur(response)

        self.assertFalse(result["rateLimit"])
        self.assertTrue(result["exists"])
