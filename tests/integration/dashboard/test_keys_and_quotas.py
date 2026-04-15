from pathlib import Path

from tests.integration.helpers import (
    SEEDED_PROJECT_NAMES,
    auth_headers,
    load_mapping,
    post_chat_completion,
    create_api_key,
    create_quota,
    delete_api_key,
    delete_quota,
    find_limit_id_by_name,
    get_all_projects,
    get_limit_types,
    get_project_id_by_name,
)


def _load_chat_request(completions_dir: Path) -> dict:
    mapping = load_mapping(completions_dir, "mock_completion1")
    request_data = mapping.get("request")
    assert request_data is not None, "Missing mock_completion1 request payload"
    return request_data


def test_keys_and_quotas_key_access_then_quota_limit_enforced(
    dashboard_base_url: str,
    completions_url: str,
    admin_token: str,
    dashboard_request_headers: dict[str, str],
    completions_dir: Path,
):
    headers = auth_headers(admin_token, dashboard_request_headers)
    request_data = _load_chat_request(completions_dir)

    projects = get_all_projects(dashboard_base_url, headers)
    assert SEEDED_PROJECT_NAMES.issubset({project.get("name") for project in projects})
    project_id = get_project_id_by_name(projects, "Test Project 1")

    created_key_resp = create_api_key(
        dashboard_base_url,
        headers,
        project_id=project_id,
        name="IT Key",
    )
    created_key = created_key_resp.json()
    api_key = created_key.get("api_key")
    key_id = int(created_key["id"])
    assert api_key, "API key response did not include the raw api_key value"

    quota_id = None

    try:
        first_access_resp = post_chat_completion(completions_url, api_key, request_data)
        assert first_access_resp.status_code == 200

        limit_types = get_limit_types(dashboard_base_url, headers)
        request_limit_id = find_limit_id_by_name(limit_types, "Request Limit")

        quota_resp = create_quota(
            dashboard_base_url,
            headers,
            key_id=key_id,
            limit_id=request_limit_id,
            limit_value=1,
            period="day",
        )
        quota_id = int(quota_resp.json()["id"])

        second_access_resp = post_chat_completion(completions_url, api_key, request_data)
        assert second_access_resp.status_code == 200

        third_access_resp = post_chat_completion(completions_url, api_key, request_data)
        assert third_access_resp.status_code == 429
        assert third_access_resp.json().get("detail") == "Quota exceeded."

    finally:
        if quota_id is not None:
            delete_quota_resp = delete_quota(dashboard_base_url, headers, quota_id)
            assert delete_quota_resp.status_code == 200, (
                f"Quota delete failed: {delete_quota_resp.status_code} {delete_quota_resp.text}"
            )

        delete_key_resp = delete_api_key(dashboard_base_url, headers, key_id)
        assert delete_key_resp.status_code == 200, f"Key delete failed: {delete_key_resp.status_code} {delete_key_resp.text}"
