# -*- coding: utf-8 -*-
import os
import re
import trio
import httpx
from holehe.defense import RequestPacer, RateLimitedException, get_backoff_delay

# Exceptions that represent connection blocks or proxy failures
CONNECTION_BLOCK_ERRORS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.NetworkError,
    httpx.ProxyError,
    httpx.RemoteProtocolError,
)


class ProxyRotator:
    """
    Manages a pool of HTTP/SOCKS5 proxies with round-robin distribution
    and immediate rotation upon HTTP 429 or connection block detection.
    """
    def __init__(self, proxy: str | None = None, proxy_file: str | None = None):
        self.proxies: list[str] = []
        self.lock = trio.Lock()
        self.index = 0

        if proxy and proxy.strip():
            self.proxies.append(self._normalize_proxy(proxy))

        if proxy_file and os.path.isfile(proxy_file):
            with open(proxy_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.proxies.append(self._normalize_proxy(line))

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for p in self.proxies:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        self.proxies = deduped

    @staticmethod
    def _normalize_proxy(p: str) -> str:
        p = p.strip()
        if not re.match(r'^(https?|socks5|socks5h)://', p, re.IGNORECASE):
            return f"http://{p}"
        return p

    def has_proxies(self) -> bool:
        return len(self.proxies) > 0

    async def get_next_proxy(self) -> str | None:
        """Round-robin selection per site request."""
        if not self.proxies:
            return None
        async with self.lock:
            p = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            return p

    async def mark_bad_and_rotate(self, current_proxy: str | None = None) -> str | None:
        """
        Immediately rotate to a fresh proxy whenever an HTTP 429 or connection block is detected.
        """
        if not self.proxies:
            return None
        async with self.lock:
            if current_proxy and current_proxy in self.proxies:
                curr_idx = self.proxies.index(current_proxy)
                next_idx = (curr_idx + 1) % len(self.proxies)
                self.index = (next_idx + 1) % len(self.proxies)
                return self.proxies[next_idx]
            else:
                p = self.proxies[self.index % len(self.proxies)]
                self.index += 1
                return p


class SiteClient:
    """
    Site-scoped HTTP client wrapping httpx.AsyncClient with:
    1. Human-like pacing jitter (0.5s - 1.8s) between outbound requests.
    2. Automatic backoff and retry wrapper on HTTP 429 (Retry-After or 2s->4s->8s).
    3. Proxy rotation upon 429 or connection block.
    4. Clean session cookie persistence across redirects and retries.
    """
    def __init__(
        self,
        rotator: ProxyRotator,
        pacer: RequestPacer,
        timeout: int = 10,
        initial_proxy: str | None = None
    ):
        self.rotator = rotator
        self.pacer = pacer
        self.timeout = timeout
        self.current_proxy = initial_proxy
        self._cookies = httpx.Cookies()
        self._client: httpx.AsyncClient | None = None
        self._init_inner_client()

    def _init_inner_client(self):
        kwargs = {
            "timeout": self.timeout,
            "cookies": self._cookies,
            "follow_redirects": True
        }
        if self.current_proxy:
            kwargs["proxy"] = self.current_proxy
        self._client = httpx.AsyncClient(**kwargs)

    async def _rotate_proxy(self):
        """Switches to the next proxy from rotator while preserving cookies."""
        if self._client:
            try:
                # Merge existing cookies before closing
                self._cookies.update(self._client.cookies)
                await self._client.aclose()
            except Exception:
                pass
        self.current_proxy = await self.rotator.mark_bad_and_rotate(self.current_proxy)
        self._init_inner_client()

    @property
    def cookies(self) -> httpx.Cookies:
        if self._client:
            return self._client.cookies
        return self._cookies

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        max_retries = 3
        last_exception = None

        for retry_count in range(max_retries + 1):
            # 1. Pacing delay jitter before each outbound request
            await self.pacer.pace()

            try:
                if self._client is None:
                    self._init_inner_client()

                response = await self._client.request(method, url, **kwargs)

                # Check for HTTP 429
                if response.status_code == 429:
                    if retry_count < max_retries:
                        # Rotate proxy immediately if proxy rotation configured
                        if self.rotator.has_proxies():
                            await self._rotate_proxy()

                        # Determine backoff duration (Retry-After header or exponential backoff)
                        retry_after_hdr = response.headers.get("Retry-After")
                        backoff = get_backoff_delay(retry_count + 1, retry_after_hdr)
                        await trio.sleep(backoff)
                        continue
                    else:
                        # All 3 retries exhausted and limit persists
                        raise RateLimitedException(response=response)

                # Request succeeded (non-429)
                self._cookies.update(self._client.cookies)
                return response

            except RateLimitedException:
                # Re-raise RateLimitedException directly to bubble up to launch_module
                raise

            except CONNECTION_BLOCK_ERRORS as ce:
                last_exception = ce
                if self.rotator.has_proxies() and retry_count < max_retries:
                    # Immediately rotate proxy on connection block and retry
                    await self._rotate_proxy()
                    backoff = get_backoff_delay(retry_count + 1)
                    await trio.sleep(backoff)
                    continue
                else:
                    if retry_count == max_retries:
                        raise
                    # Non-proxy retry with backoff
                    backoff = get_backoff_delay(retry_count + 1)
                    await trio.sleep(backoff)
                    continue

        if last_exception:
            raise last_exception
        raise RateLimitedException()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("POST", url, **kwargs)

    async def head(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("HEAD", url, **kwargs)

    async def aclose(self):
        if self._client:
            try:
                await self._client.aclose()
            except Exception:
                pass
            self._client = None


class ClientManager:
    """Factory and manager for site-scoped clients."""
    def __init__(
        self,
        proxy: str | None = None,
        proxy_file: str | None = None,
        timeout: int = 10,
        min_delay: float = 0.5,
        max_delay: float = 1.8
    ):
        self.rotator = ProxyRotator(proxy=proxy, proxy_file=proxy_file)
        self.pacer = RequestPacer(min_delay=min_delay, max_delay=max_delay)
        self.timeout = timeout

    async def create_client(self) -> SiteClient:
        initial_proxy = await self.rotator.get_next_proxy()
        return SiteClient(
            rotator=self.rotator,
            pacer=self.pacer,
            timeout=self.timeout,
            initial_proxy=initial_proxy
        )
