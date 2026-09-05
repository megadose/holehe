# -*- coding: utf-8 -*-
import email.utils
from datetime import datetime
import random
import trio


class RateLimitedException(BaseException):
    """
    Exception raised when an HTTP 429 response persists after all retries.
    Inherits from BaseException so blanket 'except Exception:' blocks in site modules
    cannot unintentionally swallow rate limit detections.
    """
    def __init__(self, response=None, message="HTTP 429: Rate limit exceeded after retries"):
        super().__init__(message)
        self.response = response
        self.message = message

    def __str__(self):
        return self.message


class RequestPacer:
    """
    Enforces a randomized, human-like delay between outbound requests across workers.
    Default jitter: 0.5s to 1.8s.
    """
    def __init__(self, min_delay: float = 0.5, max_delay: float = 1.8):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.lock = trio.Lock()
        self.last_request_time = 0.0

    async def pace(self):
        async with self.lock:
            now = trio.current_time()
            if self.last_request_time > 0:
                elapsed = now - self.last_request_time
                delay = random.uniform(self.min_delay, self.max_delay)
                if elapsed < delay:
                    await trio.sleep(delay - elapsed)
            self.last_request_time = trio.current_time()


def parse_retry_after(header_val: str | None) -> float | None:
    """
    Inspects Retry-After header and returns the wait duration in seconds,
    or None if missing/invalid.
    """
    if not header_val:
        return None
    val_str = str(header_val).strip()

    # Case 1: Seconds as integer or float
    try:
        val = float(val_str)
        if val >= 0:
            return min(val, 60.0)  # Ceiling at 60s to prevent indefinite hangs
    except ValueError:
        pass

    # Case 2: HTTP-date format (e.g. 'Wed, 21 Oct 2026 07:28:00 GMT')
    try:
        dt = email.utils.parsedate_to_datetime(val_str)
        if dt is not None:
            now = datetime.now(dt.tzinfo)
            delta = (dt - now).total_seconds()
            if delta > 0:
                return min(delta, 60.0)
    except Exception:
        pass

    return None


def get_backoff_delay(retry_count: int, header_val: str | None = None) -> float:
    """
    Computes backoff delay:
    1. Uses Retry-After header duration if present and valid.
    2. Otherwise executes exponential backoff: 2s -> 4s -> 8s (capped at 8s for 3 retries).
    """
    retry_after = parse_retry_after(header_val)
    if retry_after is not None:
        return retry_after
    
    # Exponential backoff: retry 1 -> 2s, retry 2 -> 4s, retry 3 -> 8s
    step = max(1, retry_count)
    return float(2 ** step)
