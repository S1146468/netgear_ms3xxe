def test_endpoint_aliases_point_to_real_endpoints():
    from netgear_ms3xxe.endpoints import ENDPOINTS, ALIASES

    for alias, canonical in ALIASES.items():
        assert canonical in ENDPOINTS, f"Alias {alias!r} points to missing endpoint {canonical!r}"
