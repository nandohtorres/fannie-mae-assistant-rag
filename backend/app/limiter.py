from slowapi import Limiter
from slowapi.util import get_remote_address

# Single shared limiter instance — imported by main.py (to register it) and
# by routers that need to apply rate limit decorators.
limiter = Limiter(key_func=get_remote_address)
