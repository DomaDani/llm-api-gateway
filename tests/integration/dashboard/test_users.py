import requests

from tests.integration.helpers import (
    auth_headers,
    delete_user,
    find_user_id_by_email,
    get_users,
    login,
    register_user,
)


def _new_user_identity(prefix: str = "it-user") -> tuple[str, str]:
    """Build deterministic email and username values for temporary test users."""

    return f"{prefix}@example.com", prefix


def _cleanup_user_by_email(dashboard_base_url: str, headers: dict[str, str], email: str) -> None:
    """Remove all users matching the provided email to keep tests idempotent."""

    users = get_users(dashboard_base_url, headers)
    matching = [user for user in users if user.get("email") == email]
    for user in matching:
        resp = delete_user(dashboard_base_url, headers, int(user["id"]))
        assert resp.status_code in (200, 404), f"Cleanup failed: {resp.status_code} {resp.text}"


def test_users_register_with_mandated_reset(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify admin registration creates a user and mandates password reset when requested."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    email, username = _new_user_identity("register-mandate")
    password = "InitPass123"

    try:
        resp = register_user(
            dashboard_base_url,
            headers,
            email=email,
            username=username,
            password=password,
            mandate_reset=True,
        )
        assert "registered successfully" in resp.json().get("message", "").lower()

        users = get_users(dashboard_base_url, headers)
        new_user_id = find_user_id_by_email(users, email)
        assert isinstance(new_user_id, int)

    finally:
        _cleanup_user_by_email(dashboard_base_url, headers, email)


def test_users_me_shows_new_user_and_password_expired_when_mandated(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify a mandated-reset user can authenticate and sees password-expired state in /users/me."""

    admin_headers = auth_headers(admin_token, dashboard_request_headers)
    email, username = _new_user_identity("me-check")
    password = "InitPass123"

    try:
        register_user(
            dashboard_base_url,
            admin_headers,
            email=email,
            username=username,
            password=password,
            mandate_reset=True,
        )

        login_resp = login(dashboard_base_url, dashboard_request_headers, email=email, password=password)
        user_token = login_resp.json().get("access_token")
        assert user_token

        me_headers = {**dashboard_request_headers, "Authorization": f"Bearer {user_token}"}
        me_resp = requests.get(f"{dashboard_base_url}/users/me", headers=me_headers, timeout=10)
        assert me_resp.status_code == 200

        me_payload = me_resp.json()
        assert me_payload.get("email") == email
        assert me_payload.get("username") == username
        assert me_payload.get("is_password_expired") is True

    finally:
        _cleanup_user_by_email(dashboard_base_url, admin_headers, email)


def test_users_admin_can_change_password_for_user(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify admin password change invalidates old password and allows login with the new one."""

    admin_headers = auth_headers(admin_token, dashboard_request_headers)
    email, username = _new_user_identity("password-change")
    initial_password = "InitPass123"
    new_password = "ChangedPass456"

    try:
        register_user(
            dashboard_base_url,
            admin_headers,
            email=email,
            username=username,
            password=initial_password,
            mandate_reset=True,
        )

        users = get_users(dashboard_base_url, admin_headers)
        new_user_id = find_user_id_by_email(users, email)

        change_resp = requests.put(
            f"{dashboard_base_url}/users/change-password",
            headers=admin_headers,
            json={
                "user_id": new_user_id,
                "new_password": new_password,
                "new_password_confirm": new_password,
                "mandate_reset": False,
            },
            timeout=10,
        )
        assert change_resp.status_code == 200, f"Password change failed: {change_resp.status_code} {change_resp.text}"

        wrong_login = requests.post(
            f"{dashboard_base_url}/auth/login",
            headers=dashboard_request_headers,
            json={"email": email, "password": initial_password},
            timeout=10,
        )
        assert wrong_login.status_code == 400

        login_resp = login(dashboard_base_url, dashboard_request_headers, email=email, password=new_password)
        assert isinstance(login_resp.json().get("access_token"), str)

    finally:
        _cleanup_user_by_email(dashboard_base_url, admin_headers, email)


def test_users_admin_can_delete_user(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify admin can delete a user and receives not-found on repeated delete."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    email, username = _new_user_identity("delete-user")
    password = "InitPass123"

    register_user(
        dashboard_base_url,
        headers,
        email=email,
        username=username,
        password=password,
        mandate_reset=False,
    )

    users = get_users(dashboard_base_url, headers)
    user_id = find_user_id_by_email(users, email)

    delete_resp = delete_user(dashboard_base_url, headers, user_id)
    assert delete_resp.status_code == 200
    assert "deleted successfully" in delete_resp.json().get("message", "").lower()

    delete_again_resp = delete_user(dashboard_base_url, headers, user_id)
    assert delete_again_resp.status_code == 404
    assert "not found" in delete_again_resp.json().get("detail", "").lower()


def test_users_register_invalid_email_returns_verbose_422_detail(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify invalid registration payload returns readable validation detail text."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    resp = requests.post(
        f"{dashboard_base_url}/auth/register",
        headers=headers,
        json={
            "email": "not-an-email",
            "username": "invalid-email-user",
            "password": "InitPass123",
            "mandate_reset": False,
        },
        timeout=10,
    )

    assert resp.status_code == 422
    detail = resp.json().get("detail")
    assert isinstance(detail, str)
    assert "email" in detail.lower()
