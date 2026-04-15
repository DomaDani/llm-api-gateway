import requests
from pathlib import Path
from tests.integration.helpers import bearer_headers, build_chat_url, load_mapping

def _load_request_and_expected(completions_dir: Path) -> tuple[dict, dict]:
    mapping = load_mapping(completions_dir, "mock_completion1")
    request_data = mapping.get("request")
    expected_response = mapping.get("completion")
    return request_data, expected_response


def _build_chat_url(completions_url: str) -> str:
    return build_chat_url(completions_url)


def _limited_headers(limited_api_key: str) -> dict[str, str]:
    return bearer_headers(limited_api_key)


def test_quota_immediate_over_limit_returns_429(completions_url: str, limited_api_key: str, completions_dir: Path):
    request_data, _ = _load_request_and_expected(completions_dir)

    url = _build_chat_url(completions_url)
    headers = _limited_headers(limited_api_key)

    body = {
        "model": request_data["model"],
        "messages": request_data["messages"],
        "temperature": request_data["temperature"],
        "max_tokens": 5000,
    }
    resp = requests.post(url, headers=headers, json=body)

    assert resp.status_code == 429
    response = resp.json()
    assert response["detail"] == "Quota exceeded."


def test_quota_within_limit_then_next_request_exceeds_remaining_quota(
    completions_url: str,
    limited_api_key: str,
    completions_dir: Path,
):
    request_data, expected_response = _load_request_and_expected(completions_dir)

    url = f"{completions_url}/chat/completions"
    headers = _limited_headers(limited_api_key)
    # First request is expected to be within the remaining quota.
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 200

    response = resp.json()
    response["id"] = expected_response["id"]
    assert response == expected_response
    # The immediate next request should exceed the remaining quota.
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 429
    response = resp.json()
    assert response["detail"] == "Quota exceeded."