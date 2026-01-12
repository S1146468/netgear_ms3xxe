# netgear_ms3xxe/profiles/registry.py
from __future__ import annotations

from .base import GenericProfile, SwitchProfile
from .ms305e import MS305E_PROFILE
from .ms308e import MS308E_PROFILE


KNOWN_PROFILES: list[SwitchProfile] = [
    MS305E_PROFILE,
    MS308E_PROFILE,
]


def detect_profile(model_number: str) -> SwitchProfile:
    for p in KNOWN_PROFILES:
        if p.matches(model_number):
            return p

    # Unknown model, but we still want a usable client if API matches.
    # Capabilities are intentionally None.
    return GenericProfile(
        backend_id="ms3xxe-react",
        model_numbers=(model_number,),
        display_name=f"NETGEAR {model_number}",
        expected_port_count=None,
        expected_lag_group_count=None,
    )
