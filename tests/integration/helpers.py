from pathlib import Path
import time

import requests

from tests.tools import load_mappings_from_dir


SEEDED_PROJECT_NAMES = {"Test Project 1", "Test Project 2"}
SEEDED_MANAGER_USERNAME = "GipszJakab38"
SEEDED_MEMBER_USERNAME = "JonAHegyrol"


def wait_for_health(
    url: str,
    timeout: int = 30,
    interval: float = 1.0,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    """
    Wait until a health endpoint responds with HTTP 200.

    Parameters
    ----------
    - url: The health-check URL to poll.
    - timeout: Maximum wait time in seconds.
    - interval: Sleep interval in seconds between retries.
    - headers: Optional HTTP headers sent with each request.

    Returns
    -------
    - The successful HTTP response with status code 200.
    """
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


def build_chat_url(completions_url: str) -> str:
    """
    Build the chat completions endpoint URL from a base completions URL.

    Parameters
    ----------
    - completions_url: The base URL prefix for completions requests.

    Returns
    -------
    - The fully qualified chat completions endpoint URL.
    """
    return f"{completions_url}/chat/completions"


def bearer_headers(token: str) -> dict[str, str]:
    """
    Build Authorization headers for bearer token authentication.

    Parameters
    ----------
    - token: The bearer token value.

    Returns
    -------
    - A headers dictionary containing the Authorization header.
    """
    return {"Authorization": f"Bearer {token}"}


def post_chat_completion(completions_url: str, api_key: str, request_data: dict) -> requests.Response:
    """
    Send a chat completion request to the gateway completions endpoint.

    Parameters
    ----------
    - completions_url: The base URL prefix for completions requests.
    - api_key: The API key used as a bearer token.
    - request_data: The JSON payload for the completion request.

    Returns
    -------
    - The HTTP response returned by the completions endpoint.
    """
    return requests.post(
        build_chat_url(completions_url),
        headers=bearer_headers(api_key),
        json=request_data,
        timeout=10,
    )


def load_mapping(completions_dir: Path, mapping_name: str) -> dict:
    """
    Load a named mock completion mapping from the fixtures directory.

    Parameters
    ----------
    - completions_dir: Directory containing completion mapping JSON files.
    - mapping_name: File stem of the mapping to load.

    Returns
    -------
    - The mapping dictionary, or an empty dictionary if not found.
    """
    mappings = load_mappings_from_dir(completions_dir, mapping_name)
    return mappings.get(mapping_name, {})


def auth_headers(admin_token: str, dashboard_request_headers: dict[str, str]) -> dict[str, str]:
    """
    Merge dashboard request headers with an admin bearer authorization header.

    Parameters
    ----------
    - admin_token: Access token for an authenticated administrator.
    - dashboard_request_headers: Baseline request headers required by dashboard routes.

    Returns
    -------
    - A headers dictionary with the Authorization header included.
    """
    return {**dashboard_request_headers, "Authorization": f"Bearer {admin_token}"}


def login(
    dashboard_base_url: str,
    dashboard_request_headers: dict[str, str],
    email: str,
    password: str,
    expected_status: int = 200,
) -> requests.Response:
    """
    Authenticate against the dashboard login endpoint and assert expected status.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - dashboard_request_headers: Required dashboard request headers.
    - email: Login email address.
    - password: Login password.
    - expected_status: Expected HTTP status code.

    Returns
    -------
    - The HTTP response from the login endpoint.
    """
    resp = requests.post(
        f"{dashboard_base_url}/auth/login",
        headers=dashboard_request_headers,
        json={"email": email, "password": password},
        timeout=10,
    )
    assert resp.status_code == expected_status, f"Login failed: {resp.status_code} {resp.text}"
    return resp


def get_users(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    """
    Fetch all users from the dashboard users listing endpoint.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.

    Returns
    -------
    - A list of user dictionaries.
    """
    resp = requests.get(f"{dashboard_base_url}/users/everyone", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch users: {resp.status_code} {resp.text}"
    return resp.json()


def find_user_id_by_username(users: list[dict], username: str) -> int:
    """
    Find a user ID in a user list by username.

    Parameters
    ----------
    - users: List of user dictionaries.
    - username: Username to search for.

    Returns
    -------
    - The matching user ID.
    """
    for user in users:
        if user.get("username") == username:
            return int(user["id"])
    raise AssertionError(f"Could not find user '{username}'")


def find_user_id_by_email(users: list[dict], email: str) -> int:
    """
    Find a user ID in a user list by email address.

    Parameters
    ----------
    - users: List of user dictionaries.
    - email: Email address to search for.

    Returns
    -------
    - The matching user ID.
    """
    for user in users:
        if user.get("email") == email:
            return int(user["id"])
    raise AssertionError(f"Could not find user with email '{email}'")


def register_user(
    dashboard_base_url: str,
    headers: dict[str, str],
    email: str,
    username: str,
    password: str,
    mandate_reset: bool,
) -> requests.Response:
    """
    Register a user through the dashboard authentication API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - email: New user's email address.
    - username: New user's username.
    - password: Initial password for the user.
    - mandate_reset: Whether the user must reset password on first login.

    Returns
    -------
    - The HTTP response from the register endpoint.
    """
    resp = requests.post(
        f"{dashboard_base_url}/auth/register",
        headers=headers,
        json={
            "email": email,
            "username": username,
            "password": password,
            "mandate_reset": mandate_reset,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"User register failed: {resp.status_code} {resp.text}"
    return resp


def delete_user(dashboard_base_url: str, headers: dict[str, str], user_id: int) -> requests.Response:
    """
    Delete a user through the dashboard users API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - user_id: Identifier of the user to delete.

    Returns
    -------
    - The HTTP response from the delete endpoint.
    """
    return requests.delete(
        f"{dashboard_base_url}/users/delete",
        headers=headers,
        json={"user_id": user_id},
        timeout=10,
    )


def get_all_projects(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    """
    Fetch all projects from the dashboard projects endpoint.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.

    Returns
    -------
    - A list of project dictionaries.
    """
    resp = requests.get(f"{dashboard_base_url}/projects/all", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch projects: {resp.status_code} {resp.text}"
    return resp.json()


def get_project_id_by_name(projects: list[dict], project_name: str) -> int:
    """
    Find a project ID in a project list by name.

    Parameters
    ----------
    - projects: List of project dictionaries.
    - project_name: Project name to search for.

    Returns
    -------
    - The matching project ID.
    """
    for project in projects:
        if project.get("name") == project_name:
            return int(project["id"])
    raise AssertionError(f"Could not find project '{project_name}'")


def create_project(
    dashboard_base_url: str,
    headers: dict[str, str],
    project_name: str,
    manager_id: int,
) -> requests.Response:
    """
    Create a project through the dashboard projects API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - project_name: Name for the new project.
    - manager_id: User ID assigned as project manager.

    Returns
    -------
    - The HTTP response from the create endpoint.
    """
    resp = requests.post(
        f"{dashboard_base_url}/projects/create",
        headers=headers,
        json={"name": project_name, "manager_id": manager_id},
        timeout=10,
    )
    assert resp.status_code == 200, f"Project create failed: {resp.status_code} {resp.text}"
    return resp


def delete_project(dashboard_base_url: str, headers: dict[str, str], project_id: int) -> requests.Response:
    """
    Archive or delete a project through the dashboard projects API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - project_id: Identifier of the project to delete.

    Returns
    -------
    - The HTTP response from the delete endpoint.
    """
    return requests.delete(
        f"{dashboard_base_url}/projects/delete",
        headers=headers,
        json={"project_id": project_id},
        timeout=10,
    )


def get_limit_types(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    """
    Fetch available quota limit types from the dashboard API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.

    Returns
    -------
    - A list of quota limit type dictionaries.
    """
    resp = requests.get(f"{dashboard_base_url}/quotas/limit-types", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch limit types: {resp.status_code} {resp.text}"
    return resp.json()


def find_limit_id_by_name(limit_types: list[dict], limit_name: str) -> int:
    """
    Find a quota limit type ID by its name.

    Parameters
    ----------
    - limit_types: List of limit type dictionaries.
    - limit_name: Limit type name to search for.

    Returns
    -------
    - The matching limit type ID.
    """
    for limit_type in limit_types:
        if limit_type.get("name") == limit_name:
            return int(limit_type["id"])
    raise AssertionError(f"Could not find limit type '{limit_name}'")


def create_api_key(
    dashboard_base_url: str,
    headers: dict[str, str],
    project_id: int,
    name: str,
) -> requests.Response:
    """
    Create an API key through the dashboard keys API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - project_id: Project ID the API key will belong to.
    - name: Human-readable API key label.

    Returns
    -------
    - The HTTP response from the create key endpoint.
    """
    resp = requests.post(
        f"{dashboard_base_url}/keys/create",
        headers=headers,
        json={"project_id": project_id, "name": name},
        timeout=10,
    )
    assert resp.status_code == 200, f"API key create failed: {resp.status_code} {resp.text}"
    return resp


def delete_api_key(dashboard_base_url: str, headers: dict[str, str], key_id: int) -> requests.Response:
    """
    Delete an API key through the dashboard keys API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - key_id: Identifier of the API key to delete.

    Returns
    -------
    - The HTTP response from the delete key endpoint.
    """
    return requests.delete(
        f"{dashboard_base_url}/keys/delete",
        headers=headers,
        json={"key_id": key_id},
        timeout=10,
    )


def create_quota(
    dashboard_base_url: str,
    headers: dict[str, str],
    *,
    key_id: int | None = None,
    project_id: int | None = None,
    user_id: int | None = None,
    limit_id: int,
    limit_value: float,
    period: str,
) -> requests.Response:
    """
    Create a quota through the dashboard quotas API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - key_id: Optional API key ID target for the quota.
    - project_id: Optional project ID target for the quota.
    - user_id: Optional user ID target for the quota.
    - limit_id: Limit type identifier.
    - limit_value: Numeric quota amount.
    - period: Quota period value as API string.

    Returns
    -------
    - The HTTP response from the quota create endpoint.
    """
    resp = requests.post(
        f"{dashboard_base_url}/quotas/create",
        headers=headers,
        json={
            "project_id": project_id,
            "user_id": user_id,
            "key_id": key_id,
            "limit_id": limit_id,
            "limit_value": limit_value,
            "period": period,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"Quota create failed: {resp.status_code} {resp.text}"
    return resp


def delete_quota(dashboard_base_url: str, headers: dict[str, str], quota_id: int) -> requests.Response:
    """
    Delete a quota through the dashboard quotas API.

    Parameters
    ----------
    - dashboard_base_url: Base URL of the dashboard backend service.
    - headers: Authenticated request headers.
    - quota_id: Identifier of the quota to delete.

    Returns
    -------
    - The HTTP response from the quota delete endpoint.
    """
    return requests.delete(
        f"{dashboard_base_url}/quotas/delete",
        headers=headers,
        json={"id": quota_id},
        timeout=10,
    )
