# netgear_ms3xxe/profiles/ms308e.py
from .base import SwitchProfile

MS308E_PROFILE = SwitchProfile(
    backend_id="ms3xxe-react",
    model_numbers=("MS308E",),
    display_name="NETGEAR MS308E",
    expected_port_count=8,
    expected_lag_group_count=4,
)
