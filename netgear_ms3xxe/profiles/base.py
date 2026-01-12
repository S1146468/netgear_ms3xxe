# netgear_ms3xxe/profiles/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class SwitchProfile:
    """
    Per-model metadata/capabilities for switches that share the same backend.

    IMPORTANT:
    - This must NOT perform HTTP calls.
    - It is allowed to encode known constraints (port counts, lag group slots)
      for models we have *observed*.
    """
    backend_id: str                     # e.g. "ms3xxe-react"
    model_numbers: Tuple[str, ...]      # e.g. ("MS308E",)
    display_name: str                   # e.g. "NETGEAR MS308E"
    expected_port_count: Optional[int] = None
    expected_lag_group_count: Optional[int] = None

    def matches(self, model_number: str) -> bool:
        return model_number in self.model_numbers


@dataclass(frozen=True)
class GenericProfile(SwitchProfile):
    """
    Fallback when model is unknown but backend appears compatible.
    """
    pass
