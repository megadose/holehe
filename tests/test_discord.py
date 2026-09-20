import unittest

import httpx
import trio

from holehe.modules.social_media.discord import discord


def email_errors(*codes):
    return {
        "code": 50035,
        "errors": {"email": {"_errors": [{"code": code} for code in codes]}},
    }


class DiscordTests(unittest.TestCase):
    def check_response(self, response, exists=False):
        async def run():
            out = []
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(lambda request: response)
            ) as client:
                await discord("test@example.com", client, out)
            self.assertEqual(out, [{
                "name": "discord",
                "domain": "discord.com",
                "method": "register",
                "frequent_rate_limit": False,
                "rateLimit": not exists,
                "exists": exists,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None,
            }])

        trio.run(run)

    def test_registered_email(self):
        self.check_response(
            httpx.Response(400, json=email_errors("EMAIL_ALREADY_REGISTERED")),
            exists=True,
        )

    def test_registered_error_need_not_be_first(self):
        self.check_response(
            httpx.Response(400, json=email_errors(
                "OTHER_ERROR", "EMAIL_ALREADY_REGISTERED")),
            exists=True,
        )

    def test_captcha_is_inconclusive(self):
        for payload in (
            {"captcha_key": ["captcha-required"]},
            {"captcha_key": ["captcha-required"], "code": 50035},
            {"captcha_key": ["invalid-input-response"]},
        ):
            with self.subTest(payload=payload):
                self.check_response(httpx.Response(400, json=payload))

    def test_other_validation_errors_are_inconclusive(self):
        for payload in (
            email_errors("EMAIL_INVALID"),
            email_errors("UNKNOWN_ERROR"),
            email_errors(),
            {"code": 50035, "errors": {"username": {"_errors": []}}},
        ):
            with self.subTest(payload=payload):
                self.check_response(httpx.Response(400, json=payload))

    def test_rate_limit_and_http_failures_are_inconclusive(self):
        for status in (403, 429, 500, 502):
            with self.subTest(status=status):
                self.check_response(httpx.Response(
                    status, json={"message": "Blocked", "retry_after": 10}))

    def test_http_failure_does_not_confirm_registration(self):
        self.check_response(httpx.Response(
            429, json=email_errors("EMAIL_ALREADY_REGISTERED")))

    def test_malformed_and_unexpected_responses_are_inconclusive(self):
        for payload in (None, [], "unexpected", {},
                        {"errors": None},
                        {"errors": {"email": {"_errors": None}}},
                        {"errors": {"email": {"_errors": [None]}}}):
            with self.subTest(payload=payload):
                self.check_response(httpx.Response(400, json=payload))
        self.check_response(httpx.Response(400, text="not JSON"))
        self.check_response(httpx.Response(200, json={}))


if __name__ == "__main__":
    unittest.main()
