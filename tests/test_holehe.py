# -*- coding: utf-8 -*-
import unittest
import tempfile
import os
import trio
import httpx
from argparse import Namespace

from holehe.defense import (
    RateLimitedException,
    RequestPacer,
    parse_retry_after,
    get_backoff_delay,
)
from holehe.proxy import (
    ProxyRotator,
    SiteClient,
    ClientManager,
)
from holehe.core import (
    get_functions,
    import_submodules,
    launch_module,
    MODULE_DOMAINS,
    __version__,
)


class TestDefenseMechanisms(unittest.TestCase):
    def test_rate_limited_exception_not_caught_by_exception(self):
        """Verify RateLimitedException inherits from BaseException and bypasses 'except Exception'."""
        self.assertTrue(issubclass(RateLimitedException, BaseException))
        self.assertFalse(issubclass(RateLimitedException, Exception))

        caught_by_generic = False
        caught_by_rate_limited = False

        try:
            try:
                raise RateLimitedException()
            except Exception:
                caught_by_generic = True
        except RateLimitedException:
            caught_by_rate_limited = True

        self.assertFalse(caught_by_generic)
        self.assertTrue(caught_by_rate_limited)

    def test_parse_retry_after_seconds(self):
        self.assertEqual(parse_retry_after("10"), 10.0)
        self.assertEqual(parse_retry_after(" 25.5 "), 25.5)
        self.assertEqual(parse_retry_after("0"), 0.0)
        self.assertIsNone(parse_retry_after(None))
        self.assertIsNone(parse_retry_after("invalid_header"))

    def test_get_backoff_delay_exponential(self):
        """Verify 2s -> 4s -> 8s exponential backoff when Retry-After is absent."""
        self.assertEqual(get_backoff_delay(1), 2.0)
        self.assertEqual(get_backoff_delay(2), 4.0)
        self.assertEqual(get_backoff_delay(3), 8.0)

    def test_get_backoff_delay_with_retry_after(self):
        """Verify Retry-After overrides exponential backoff."""
        self.assertEqual(get_backoff_delay(1, header_val="15"), 15.0)
        self.assertEqual(get_backoff_delay(2, header_val="7"), 7.0)

    def test_request_pacer(self):
        """Verify RequestPacer spaces requests by at least min_delay."""
        async def run_pacer_test():
            pacer = RequestPacer(min_delay=0.08, max_delay=0.12)
            t0 = trio.current_time()
            await pacer.pace()
            await pacer.pace()
            t1 = trio.current_time()
            self.assertGreaterEqual(t1 - t0, 0.07)

        trio.run(run_pacer_test)


class TestProxyRotation(unittest.TestCase):
    def test_proxy_normalization(self):
        r = ProxyRotator(proxy="127.0.0.1:8080")
        self.assertEqual(r.proxies[0], "http://127.0.0.1:8080")

        r2 = ProxyRotator(proxy="socks5://127.0.0.1:1080")
        self.assertEqual(r2.proxies[0], "socks5://127.0.0.1:1080")

    def test_proxy_file_loading_and_round_robin(self):
        async def run_proxy_test():
            with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
                f.write("# comment\n")
                f.write("1.1.1.1:8080\n")
                f.write("socks5://2.2.2.2:1080\n")
                f.write("http://3.3.3.3:3128\n")
                f.flush()
                fname = f.name

            try:
                rotator = ProxyRotator(proxy_file=fname)
                self.assertEqual(len(rotator.proxies), 3)

                p1 = await rotator.get_next_proxy()
                p2 = await rotator.get_next_proxy()
                p3 = await rotator.get_next_proxy()
                p4 = await rotator.get_next_proxy()

                self.assertEqual(p1, "http://1.1.1.1:8080")
                self.assertEqual(p2, "socks5://2.2.2.2:1080")
                self.assertEqual(p3, "http://3.3.3.3:3128")
                self.assertEqual(p4, "http://1.1.1.1:8080")  # wrapped around
            finally:
                if os.path.exists(fname):
                    os.remove(fname)

        trio.run(run_proxy_test)

    def test_mark_bad_and_rotate(self):
        async def run_rotate_test():
            rotator = ProxyRotator()
            rotator.proxies = ["http://proxy1:8080", "http://proxy2:8080", "http://proxy3:8080"]
            initial = await rotator.get_next_proxy()
            self.assertEqual(initial, "http://proxy1:8080")

            rotated = await rotator.mark_bad_and_rotate(initial)
            self.assertEqual(rotated, "http://proxy2:8080")

        trio.run(run_rotate_test)


class MockTransport(httpx.AsyncBaseTransport):
    def __init__(self, responses):
        self.responses = list(responses)
        self.call_count = 0

    async def handle_async_request(self, request):
        self.call_count += 1
        if self.responses:
            resp = self.responses.pop(0)
            if isinstance(resp, Exception):
                raise resp
            return resp
        return httpx.Response(200, request=request)


class TestBackoffAndRetry(unittest.TestCase):
    def test_retry_on_429_eventual_success(self):
        async def run_test():
            rotator = ProxyRotator()
            pacer = RequestPacer(min_delay=0.01, max_delay=0.02)
            site_client = SiteClient(rotator=rotator, pacer=pacer, timeout=5)

            req = httpx.Request("GET", "https://example.com")
            # 2x 429 followed by a 200
            transport = MockTransport([
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
                httpx.Response(200, json={"status": "ok"}, request=req),
            ])
            site_client._client = httpx.AsyncClient(transport=transport)

            resp = await site_client.get("https://example.com")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(transport.call_count, 3)
            await site_client.aclose()

        trio.run(run_test)

    def test_retry_on_429_exhausted_raises_rate_limited(self):
        async def run_test():
            rotator = ProxyRotator()
            pacer = RequestPacer(min_delay=0.01, max_delay=0.02)
            site_client = SiteClient(rotator=rotator, pacer=pacer, timeout=5)

            req = httpx.Request("GET", "https://example.com")
            # 4x 429 (initial + 3 retries) -> should raise RateLimitedException
            transport = MockTransport([
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
                httpx.Response(429, headers={"Retry-After": "0.01"}, request=req),
            ])
            site_client._client = httpx.AsyncClient(transport=transport)

            with self.assertRaises(RateLimitedException):
                await site_client.get("https://example.com")

            self.assertEqual(transport.call_count, 4)
            await site_client.aclose()

        trio.run(run_test)


class TestModuleFiltering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = import_submodules("holehe.modules")

    def test_filter_only_single(self):
        args = Namespace(only_modules=["twitter"], exclude_modules=None, nopasswordrecovery=False)
        funcs = get_functions(self.modules, args)
        self.assertEqual(len(funcs), 1)
        self.assertEqual(funcs[0].__name__, "twitter")

    def test_filter_only_multiple(self):
        args = Namespace(only_modules=["twitter", "instagram"], exclude_modules=None, nopasswordrecovery=False)
        funcs = get_functions(self.modules, args)
        self.assertEqual(len(funcs), 2)
        names = {f.__name__ for f in funcs}
        self.assertEqual(names, {"twitter", "instagram"})

    def test_filter_only_comma_separated(self):
        args = Namespace(only_modules=["twitter,spotify"], exclude_modules=None, nopasswordrecovery=False)
        funcs = get_functions(self.modules, args)
        self.assertEqual(len(funcs), 2)
        names = {f.__name__ for f in funcs}
        self.assertEqual(names, {"twitter", "spotify"})

    def test_filter_exclude(self):
        all_funcs = get_functions(self.modules, None)
        total_count = len(all_funcs)

        args = Namespace(only_modules=None, exclude_modules=["twitter", "instagram"], nopasswordrecovery=False)
        filtered = get_functions(self.modules, args)
        self.assertEqual(len(filtered), total_count - 2)
        filtered_names = {f.__name__ for f in filtered}
        self.assertNotIn("twitter", filtered_names)
        self.assertNotIn("instagram", filtered_names)


class TestLaunchModuleIntegration(unittest.TestCase):
    def test_launch_module_flags_rate_limited_cleanly(self):
        """Verify launch_module cleanly catches RateLimitedException and marks rate_limited."""
        async def run_test():
            async def fake_rate_limited_module(email, client, out):
                # Simulates a module where client.get triggers RateLimitedException
                raise RateLimitedException()

            fake_rate_limited_module.__name__ = "twitter"

            client_manager = ClientManager(min_delay=0.01, max_delay=0.02)
            out = []
            limiter = trio.CapacityLimiter(2)

            await launch_module(fake_rate_limited_module, "test@example.com", client_manager, out, limiter)

            self.assertEqual(len(out), 1)
            result = out[0]
            self.assertEqual(result["name"], "twitter")
            self.assertEqual(result["domain"], "twitter.com")
            self.assertTrue(result["rate_limited"])
            self.assertTrue(result["rateLimit"])
            self.assertFalse(result["error"])
            self.assertFalse(result["exists"])

        trio.run(run_test)


if __name__ == "__main__":
    unittest.main()
