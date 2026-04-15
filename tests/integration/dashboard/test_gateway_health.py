from tests.integration.helpers import wait_for_health


def test_dashboard_health_endpoint_returns_200(
    dashboard_base_url: str,
    dashboard_request_headers: dict[str, str],
    frontend_origin: str,
):
    resp = wait_for_health(f"{dashboard_base_url}/health", headers=dashboard_request_headers)
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"
    assert resp.headers.get("access-control-allow-origin") == frontend_origin
