import requests

from tests.integration.helpers import (
    SEEDED_MEMBER_USERNAME,
    SEEDED_MANAGER_USERNAME,
    SEEDED_PROJECT_NAMES,
    auth_headers,
    create_project,
    delete_project,
    find_user_id_by_username,
    get_all_projects,
    get_project_id_by_name,
    get_users,
)


def test_projects_seeded_projects_are_listed(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify seeded projects are visible through the dashboard project listing endpoint."""

    headers = auth_headers(admin_token, dashboard_request_headers)

    projects = get_all_projects(dashboard_base_url, headers)
    project_names = {project.get("name") for project in projects}

    assert SEEDED_PROJECT_NAMES.issubset(project_names)


def test_projects_create_project_then_list_contains_it(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify creating a project makes it retrievable from subsequent list calls."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    users = get_users(dashboard_base_url, headers)
    manager_id = find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)

    project_name = "IT Project"
    create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = get_all_projects(dashboard_base_url, headers)
    project_id = get_project_id_by_name(projects, project_name)

    assert isinstance(project_id, int)

    cleanup_resp = delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_add_user_to_project(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify adding a user to a project updates the project's user membership view."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    users = get_users(dashboard_base_url, headers)
    manager_id = find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)
    member_id = find_user_id_by_username(users, SEEDED_MEMBER_USERNAME)

    project_name = "IT Project AddUser"
    create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = get_all_projects(dashboard_base_url, headers)
    project_id = get_project_id_by_name(projects, project_name)

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

    cleanup_resp = delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_remove_user_from_project(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify removing a user from a project removes them from project membership results."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    users = get_users(dashboard_base_url, headers)
    manager_id = find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)
    member_id = find_user_id_by_username(users, SEEDED_MEMBER_USERNAME)

    project_name = "IT Project RemoveUser"
    create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = get_all_projects(dashboard_base_url, headers)
    project_id = get_project_id_by_name(projects, project_name)

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

    cleanup_resp = delete_project(dashboard_base_url, headers, project_id)
    assert cleanup_resp.status_code == 200, f"Cleanup delete failed: {cleanup_resp.status_code} {cleanup_resp.text}"


def test_projects_delete_project_then_second_delete_fails(
    dashboard_base_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
):
    """Verify deleting a project succeeds once and then fails on repeated deletion."""

    headers = auth_headers(admin_token, dashboard_request_headers)
    users = get_users(dashboard_base_url, headers)
    manager_id = find_user_id_by_username(users, SEEDED_MANAGER_USERNAME)

    project_name = "IT Project Delete"
    create_project(dashboard_base_url, headers, project_name, manager_id)

    projects = get_all_projects(dashboard_base_url, headers)
    project_id = get_project_id_by_name(projects, project_name)

    first_delete_resp = delete_project(dashboard_base_url, headers, project_id)
    assert first_delete_resp.status_code == 200

    second_delete_resp = delete_project(dashboard_base_url, headers, project_id)
    assert second_delete_resp.status_code == 400
    assert "already archived" in second_delete_resp.json().get("detail", "")
