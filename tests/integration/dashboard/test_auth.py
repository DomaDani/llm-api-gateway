import requests

from tests.integration.helpers import login


def test_dashboard_login_returns_bearer_token(
    dashboard_base_url: str,
    administrator_email: str,
    administrator_password: str,
    dashboard_request_headers: dict[str, str],
):
    resp = login(
        dashboard_base_url,
        dashboard_request_headers,
        email=administrator_email,
        password=administrator_password,
    )

    assert resp.status_code == 200
    payload = resp.json()
    assert payload.get("token_type") == "bearer"
    assert isinstance(payload.get("access_token"), str)
    assert payload["access_token"]


def test_dashboard_me_returns_admin_user(
    dashboard_base_url: str,
    admin_token: str,
    administrator_email: str,
    dashboard_request_headers: dict[str, str],
):
    headers = {**dashboard_request_headers, "Authorization": f"Bearer {admin_token}"}
    resp = requests.get(
        f"{dashboard_base_url}/users/me",
        headers=headers,
        timeout=10,
    )

    assert resp.status_code == 200
    payload = resp.json()
    assert payload.get("email") == administrator_email
    assert payload.get("is_admin") is True


def test_dashboard_login_rejects_wrong_password(
    dashboard_base_url: str,
    administrator_email: str,
    dashboard_request_headers: dict[str, str],
):
    resp = login(
        dashboard_base_url,
        dashboard_request_headers,
        email=administrator_email,
        password="wrong-password",
        expected_status=400,
    )

    assert resp.status_code == 400
    assert resp.json().get("detail") == "Incorrect email or password!"
