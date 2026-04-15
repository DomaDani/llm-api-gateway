from uuid import uuid4

import requests


SEEDED_PROJECT_NAMES = {"Test Project 1", "Test Project 2"}
SEEDED_MANAGER_USERNAME = "GipszJakab38"
SEEDED_MEMBER_USERNAME = "JonAHegyrol"


def _auth_headers(admin_token: str, dashboard_request_headers: dict[str, str]) -> dict[str, str]:
    return {**dashboard_request_headers, "Authorization": f"Bearer {admin_token}"}


def _get_users(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    resp = requests.get(f"{dashboard_base_url}/users/everyone", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch users: {resp.status_code} {resp.text}"
    return resp.json()


def _find_user_id_by_username(users: list[dict], username: str) -> int:
    for user in users:
        if user.get("username") == username:
            return int(user["id"])
    raise AssertionError(f"Could not find seeded user '{username}'")


def _get_all_projects(dashboard_base_url: str, headers: dict[str, str]) -> list[dict]:
    resp = requests.get(f"{dashboard_base_url}/projects/all", headers=headers, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch projects: {resp.status_code} {resp.text}"
    return resp.json()


def _get_project_id_by_name(projects: list[dict], project_name: str) -> int:
    for project in projects:
        if project.get("name") == project_name:
            return int(project["id"])
    raise AssertionError(f"Could not find project '{project_name}'")


def _create_project(
    dashboard_base_url: str,
    headers: dict[str, str],
    project_name: str,
    manager_id: int,
) -> None:
    resp = requests.post(
        f"{dashboard_base_url}/projects/create",
        headers=headers,
        json={"name": project_name, "manager_id": manager_id},
        timeout=10,
    )
    assert resp.status_code == 200, f"Project create failed: {resp.status_code} {resp.text}"


def _delete_project(dashboard_base_url: str, headers: dict[str, str], project_id: int) -> requests.Response:
    return requests.delete(
        f"{dashboard_base_url}/projects/delete",
        headers=headers,
        json={"project_id": project_id},
        timeout=10,
    )


def test_projects_seeded_projects_are_listed(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    headers = _auth_headers(admin_token, dashboard_request_headers)

    projects = _get_all_projects(dashboard_base_url, headers)
    project_names = {project.get("name") for project in projects}

    assert SEEDED_PROJECT_NAMES.issubset(project_names)


def test_projects_create_project_then_list_contains_it(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    headers = _auth_headers(admin_token, dashboard_request_headers)
    users = _get_users(dashboard_base_url, headers)
    manager_id = _find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)

    project_name = "IT Project"
    _create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = _get_all_projects(dashboard_base_url, headers)
    project_id = _get_project_id_by_name(projects, project_name)

    assert isinstance(project_id, int)

    cleanup_resp = _delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_add_user_to_project(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    headers = _auth_headers(admin_token, dashboard_request_headers)
    users = _get_users(dashboard_base_url, headers)
    manager_id = _find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)
    member_id = _find_user_id_by_username(users, SEEDED_MEMBER_USERNAME)

    project_name = "IT Project AddUser"
    _create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = _get_all_projects(dashboard_base_url, headers)
    project_id = _get_project_id_by_name(projects, project_name)

    add_resp = requests.post(
        f"{dashboard_base_url}/projects/add-user",
        headers=headers,
        json={"project_id": project_id, "user_id": member_id},
        timeout=10,
    )
    assert add_resp.status_code == 200, f"Add user failed: {add_resp.status_code} {add_resp.text}"

    users_in_project_resp = requests.get(
        f"{dashboard_base_url}/users/info",
        headers=headers,
        params={"project_id": project_id},
        timeout=10,
    )
    assert users_in_project_resp.status_code == 200
    usernames = {user.get("username") for user in users_in_project_resp.json()}
    assert SEEDED_MEMBER_USERNAME in usernames

    cleanup_resp = _delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_remove_user_from_project(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    headers = _auth_headers(admin_token, dashboard_request_headers)
    users = _get_users(dashboard_base_url, headers)
    manager_id = _find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)
    member_id = _find_user_id_by_username(users, SEEDED_MEMBER_USERNAME)

    project_name = "IT Project RemoveUser"
    _create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = _get_all_projects(dashboard_base_url, headers)
    project_id = _get_project_id_by_name(projects, project_name)

    add_resp = requests.post(
        f"{dashboard_base_url}/projects/add-user",
        headers=headers,
        json={"project_id": project_id, "user_id": member_id},
        timeout=10,
    )
    assert add_resp.status_code == 200

    remove_resp = requests.post(
        f"{dashboard_base_url}/projects/remove-user",
        headers=headers,
        json={"project_id": project_id, "user_id": member_id},
        timeout=10,
    )
    assert remove_resp.status_code == 200, f"Remove user failed: {remove_resp.status_code} {remove_resp.text}"

    users_in_project_resp = requests.get(
        f"{dashboard_base_url}/users/info",
        headers=headers,
        params={"project_id": project_id},
        timeout=10,
    )
    assert users_in_project_resp.status_code == 200
    usernames = {user.get("username") for user in users_in_project_resp.json()}
    assert SEEDED_MEMBER_USERNAME not in usernames

    cleanup_resp = _delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_delete_project_then_second_delete_fails(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    headers = _auth_headers(admin_token, dashboard_request_headers)
    users = _get_users(dashboard_base_url, headers)
    manager_id = _find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)

    project_name = "IT Project Delete"
    _create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = _get_all_projects(dashboard_base_url, headers)
    project_id = _get_project_id_by_name(projects, project_name)

    first_delete_resp = _delete_project(dashboard_base_url, headers, project_id)
    assert first_delete_resp.status_code == 200

    second_delete_resp = _delete_project(dashboard_base_url, headers, project_id)
    assert second_delete_resp.status_code == 400
    assert "already archived" in second_delete_resp.json().get("detail", "")
