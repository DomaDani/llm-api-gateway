import os
from pathlib import Path
import time

import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get(
        "BASE_URL",
        "http://docker:8000" if (os.environ.get("CI") or os.environ.get("GITLAB_CI")) else "http://localhost:8000",
    )


@pytest.fixture(scope="session")
def dashboard_base_url() -> str:
    return os.environ.get(
        "DASHBOARD_BASE_URL",
        "http://docker:8080" if (os.environ.get("CI") or os.environ.get("GITLAB_CI")) else "http://localhost:8080",
    )


@pytest.fixture(scope="session")
def administrator_email() -> str:
    return os.environ.get("ADMINISTRATOR_EMAIL", "admin@example.com")


@pytest.fixture(scope="session")
def administrator_password() -> str:
    return os.environ.get("ADMINISTRATOR_PASSWORD", "password123")


@pytest.fixture(scope="session")
def frontend_origin() -> str:
    frontend_address = os.environ.get("FRONTEND_ADDRESS", "http://localhost")
    return f"{frontend_address}:5173"


@pytest.fixture(scope="session")
def dashboard_request_headers(frontend_origin: str) -> dict[str, str]:
    return {
        "Origin": frontend_origin,
        "Referer": f"{frontend_origin}/",
    }


def _wait_for_health(url: str, timeout: int = 30, interval: float = 1.0) -> requests.Response:
    end = time.time() + timeout
    while time.time() < end:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return resp
        except requests.RequestException:
            pass
        time.sleep(interval)
    raise AssertionError(f"Timed out waiting for {url}")


@pytest.fixture(scope="session")
def admin_token(
    dashboard_base_url: str,
    administrator_email: str,
    administrator_password: str,
    dashboard_request_headers: dict[str, str],
) -> str:
    _wait_for_health(f"{dashboard_base_url}/health")
    resp = requests.post(
        f"{dashboard_base_url}/auth/login",
        headers=dashboard_request_headers,
        json={"email": administrator_email, "password": administrator_password},
        timeout=10,
    )
    assert resp.status_code == 200, f"Admin login failed: {resp.status_code} {resp.text}"

    payload = resp.json()
    token = payload.get("access_token")
    assert token, "Missing access_token in login response"
    return token

@pytest.fixture(scope="session")
def completions_url(base_url: str) -> str:
    return f"{base_url}/v1"

@pytest.fixture(scope="session")
def unlimited_api_key() -> str:
    return os.environ.get("UNLIMITED_API_KEY", "TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q")

@pytest.fixture(scope="session")
def limited_api_key() -> str:
    return os.environ.get("LIMITED_API_KEY", "WQC-GPp6L8glbHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def expired_api_key() -> str:
    return os.environ.get("EXPIRED_API_KEY", "ExpiredKey123bHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).parents[1] / "fixtures"

@pytest.fixture(scope="session")
def completions_dir(fixtures_dir: Path) -> Path:
    return fixtures_dir  / "completions"

@pytest.fixture(autouse=True, scope="session")
def sleep_between_tests():
    time.sleep(1)