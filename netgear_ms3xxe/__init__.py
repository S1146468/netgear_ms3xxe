# netgear_ms3xxe/__init__.py
from .client import NetgearSwitchClient
from .exceptions import NetgearAPIError

__all__ = ["NetgearSwitchClient", "NetgearAPIError"]
