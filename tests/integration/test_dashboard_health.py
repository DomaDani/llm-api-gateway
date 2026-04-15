import requests
import time


def _wait_for_health(
    url: str,
    timeout: int = 30,
    interval: float = 1.0,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    end = time.time() + timeout
    while time.time() < end:
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp
        except requests.RequestException:
            pass
        time.sleep(interval)
    raise AssertionError(f"Timed out waiting for {url}")


def test_dashboard_health_endpoint_returns_200(
    dashboard_base_url: str,
    dashboard_request_headers: dict[str, str],
    frontend_origin: str,
):
    resp = _wait_for_health(f"{dashboard_base_url}/health", headers=dashboard_request_headers)
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"
    assert resp.headers.get("access-control-allow-origin") == frontend_origin
