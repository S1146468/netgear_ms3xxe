# netgear_ms3xxe/profiles/__init__.py
from .base import SwitchProfile, GenericProfile
from .registry import detect_profile
from .ms305e import MS305E_PROFILE
from .ms308e import MS308E_PROFILE

__all__ = [
    "SwitchProfile",
    "GenericProfile",
    "detect_profile",
    "MS305E_PROFILE",
    "MS308E_PROFILE",
]
