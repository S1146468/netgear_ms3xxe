# netgear_ms3xxe/profiles/ms305e.py
from .base import SwitchProfile

MS305E_PROFILE = SwitchProfile(
    backend_id="ms3xxe-react",
    model_numbers=("MS305E",),
    display_name="NETGEAR MS305E",
    expected_port_count=5,
    expected_lag_group_count=2,
)
