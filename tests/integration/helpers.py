from pathlib import Path
import time

import requests

from tests.tools.load_mappings import load_mappings_from_dir


SEEDED_PROJECT_NAMES = {"Test Project 1", "Test Project 2"}
SEEDED_MANAGER_USERNAME = "GipszJakab38"
SEEDED_MEMBER_USERNAME = "JonAHegyrol"


def wait_for_health(
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


def build_chat_url(completions_url: str) -> str:
    return f"{completions_url}/chat/completions"


def bearer_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def post_chat_completion(completions_url: str, api_key: str, request_data: dict) -> requests.Response:
    return requests.post(
        build_chat_url(completions_url),
        headers=bearer_headers(api_key),
        json=request_data,
        timeout=10,
    )


def load_mapping(completions_dir: Path, mapping_name: str) -> dict:
    mappings = load_mappings_from_dir(completions_dir, mapping_name)
    return mappings.get(mapping_name, {})


def auth_headers(admin_token: str, dashboard_request_headers: dict[str, str]) -> dict[str, str]:
    return {**dashboard_request_headers, "Authorization": f"Bearer {admin_token}"}


def login(
    dashboard_base_url: str,
    dashboard_request_headers: dict[str, str],
    email: str,
    password: str,
    expected_status: int = 200,
) -> requests.Response:
    resp = requests.post(
        f"{dashboard_base_url}/auth/login",
        headers=dashboard_request_headers,
        json={"email": email, "password": password},
        timeout=10,
    )
    assert resp.status_code == expected_status, f"Login failed: {resp.status_code} {resp.text}"
    return resp


def get_users(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    resp = requests.get(f"{dashboard_base_url}/users/everyone", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch users: {resp.status_code} {resp.text}"
    return resp.json()


def find_user_id_by_username(users: list[dict], username: str) -> int:
    for user in users:
        if user.get("username") == username:
            return int(user["id"])
    raise AssertionError(f"Could not find user '{username}'")


def find_user_id_by_email(users: list[dict], email: str) -> int:
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
    return requests.delete(
        f"{dashboard_base_url}/users/delete",
        headers=headers,
        json={"user_id": user_id},
        timeout=10,
    )


def get_all_projects(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    resp = requests.get(f"{dashboard_base_url}/projects/all", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch projects: {resp.status_code} {resp.text}"
    return resp.json()


def get_project_id_by_name(projects: list[dict], project_name: str) -> int:
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
    resp = requests.post(
        f"{dashboard_base_url}/projects/create",
        headers=headers,
        json={"name": project_name, "manager_id": manager_id},
        timeout=10,
    )
    assert resp.status_code == 200, f"Project create failed: {resp.status_code} {resp.text}"
    return resp


def delete_project(dashboard_base_url: str, headers: dict[str, str], project_id: int) -> requests.Response:
    return requests.delete(
        f"{dashboard_base_url}/projects/delete",
        headers=headers,
        json={"project_id": project_id},
        timeout=10,
    )


def get_limit_types(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    resp = requests.get(f"{dashboard_base_url}/quotas/limit-types", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch limit types: {resp.status_code} {resp.text}"
    return resp.json()


def find_limit_id_by_name(limit_types: list[dict], limit_name: str) -> int:
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
    resp = requests.post(
        f"{dashboard_base_url}/keys/create",
        headers=headers,
        json={"project_id": project_id, "name": name},
        timeout=10,
    )
    assert resp.status_code == 200, f"API key create failed: {resp.status_code} {resp.text}"
    return resp


def delete_api_key(dashboard_base_url: str, headers: dict[str, str], key_id: int) -> requests.Response:
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
    return requests.delete(
        f"{dashboard_base_url}/quotas/delete",
        headers=headers,
        json={"id": quota_id},
        timeout=10,
    )
