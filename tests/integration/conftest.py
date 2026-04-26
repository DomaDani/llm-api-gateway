import os
from pathlib import Path
import time

import pytest
from tests.integration import login, wait_for_health


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the gateway base URL based on local or CI environment."""

    is_ci = bool(os.environ.get("CI") or os.environ.get("GITLAB_CI"))
    gateway_host = "docker" if is_ci else "localhost"
    gateway_port = os.environ.get("GATEWAY_PORT", "8000")
    return os.environ.get("BASE_URL", f"http://{gateway_host}:{gateway_port}")


@pytest.fixture(scope="session")
def dashboard_base_url() -> str:
    """Return the dashboard base URL based on local or CI environment."""

    is_ci = bool(os.environ.get("CI") or os.environ.get("GITLAB_CI"))
    dashboard_host = "docker" if is_ci else "localhost"
    dashboard_port = os.environ.get("DASHBOARD_BACKEND_PORT", "8080")
    return os.environ.get("DASHBOARD_BASE_URL", f"http://{dashboard_host}:{dashboard_port}")


@pytest.fixture(scope="session")
def administrator_email() -> str:
    """Return administrator email used for dashboard authentication tests."""

    return os.environ.get("ADMINISTRATOR_EMAIL", "admin@example.com")


@pytest.fixture(scope="session")
def administrator_password() -> str:
    """Return administrator password used for dashboard authentication tests."""

    return os.environ.get("ADMINISTRATOR_PASSWORD", "password123")


@pytest.fixture(scope="session")
def frontend_origin() -> str:
    """Return the frontend origin value used for CORS-sensitive dashboard calls."""

    frontend_address = os.environ.get("FRONTEND_ADDRESS", "http://localhost")
    frontend_port = os.environ.get("DASHBOARD_FRONTEND_PORT", "5173")
    return f"{frontend_address}:{frontend_port}"


@pytest.fixture(scope="session")
def dashboard_request_headers(frontend_origin: str) -> dict[str, str]:
    """Build default request headers expected by dashboard endpoints."""

    return {
        "Origin": frontend_origin,
        "Referer": f"{frontend_origin}/",
    }

@pytest.fixture(scope="session")
def admin_token(
    dashboard_base_url: str,
    administrator_email: str,
    administrator_password: str,
    dashboard_request_headers: dict[str, str],
) -> str:
    """Authenticate once per session and return an admin access token."""

    wait_for_health(f"{dashboard_base_url}/health")
    resp = login(
        dashboard_base_url,
        dashboard_request_headers,
        email=administrator_email,
        password=administrator_password,
    )

    payload = resp.json()
    token = payload.get("access_token")
    assert token, "Missing access_token in login response"
    return token

@pytest.fixture(scope="session")
def completions_url(base_url: str) -> str:
    """Return the gateway chat-completions API prefix."""

    return f"{base_url}/v1"

@pytest.fixture(scope="session")
def unlimited_api_key() -> str:
    """Return a seeded API key intended to run without quota restrictions."""

    return os.environ.get("UNLIMITED_API_KEY", "TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q")

@pytest.fixture(scope="session")
def limited_api_key() -> str:
    """Return a seeded API key with strict quota limits for quota tests."""

    return os.environ.get("LIMITED_API_KEY", "WQC-GPp6L8glbHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def expired_api_key() -> str:
    """Return a seeded API key that should be treated as expired or inactive."""

    return os.environ.get("EXPIRED_API_KEY", "ExpiredKey123bHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Return the root fixtures directory used by integration tests."""

    return Path(__file__).parents[1] / "fixtures"

@pytest.fixture(scope="session")
def completions_dir(fixtures_dir: Path) -> Path:
    """Return the completions fixture directory containing mock payload mappings."""

    return fixtures_dir  / "completions"

@pytest.fixture(autouse=True, scope="session")
def sleep_between_tests():
    """Introduce a short startup delay to reduce race conditions during test bootstrapping."""

    time.sleep(1)