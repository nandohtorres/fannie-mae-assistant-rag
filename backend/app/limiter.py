from fastapi import Request
from slowapi import Limiter


def _get_real_ip(request: Request) -> str:
    """
    Returns the real client IP, reading X-Forwarded-For when behind a reverse proxy
    (e.g. Railway). Falls back to request.client.host for local/direct connections.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host or "unknown"


# Single shared limiter instance — imported by main.py (to register it) and
# by routers that need to apply rate limit decorators.
limiter = Limiter(key_func=_get_real_ip)
